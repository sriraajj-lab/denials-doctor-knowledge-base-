#!/usr/bin/env python3
"""DenialsDoctor — Fulfillment Bridge deploy (P0 fixes).

Phases:
  0. env secrets   — INTERNAL_PROVISION_SECRET + Zoho mail vars (idempotent)
  1. backend       — provisioning.py + server.py hook (import, include, /auth/me plan) + restart + health + rollback
  2. receiver      — receiver.py (provision call + emails) + restart + health + rollback
  3. static        — welcome/set-password/login/console pages, sitemap, start.html redirects
  4. caddy         — static rewrites for /welcome /login /app, agents. vhost fix, /internal lockdown

Secrets never printed. Every phase backed up; backend/receiver auto-rollback on health failure.
"""
import json
import os
import re
import secrets as pysecrets
import sys
import time

import paramiko

PEM = "/home/z/my-project/scripts/dd-fix-key"
HOST = "134.122.2.180"
TS = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

L = "/home/z/my-project/scripts/dd-fulfillment"
LOCAL = {
    "provisioning": f"{L}/provisioning.py",
    "receiver": "/home/z/my-project/scripts/dd-dodo-webhook/receiver.py",
    "welcome": f"{L}/welcome.html",
    "setpwd": f"{L}/set-password.html",
    "login": f"{L}/login.html",
    "console": f"{L}/console.html",
}
REMOTE = {
    "provisioning": "/opt/denials-doctor-v37/src/provisioning.py",
    "server": "/opt/denials-doctor-v37/src/server.py",
    "receiver": "/opt/dd-dodo-webhook/receiver.py",
    "webroot": "/var/www/denialsdoctor",
    "start": "/var/www/denialsdoctor/start.html",
    "sitemap": "/var/www/denialsdoctor/sitemap.xml",
    "caddy": "/etc/caddy/Caddyfile",
    "backend_env": "/etc/denials-doctor/env",
    "receiver_env": "/etc/dd-dodo-webhook/env",
}

failures = []


def run(ssh, cmd, timeout=90):
    _, out, err = ssh.exec_command(cmd, timeout=timeout)
    o = out.read().decode(errors="replace")
    e = err.read().decode(errors="replace")
    code = out.channel.recv_exit_status()
    return code, o, e


def step(name, ok, detail=""):
    tag = "✓" if ok else "✗"
    print(f"{tag} {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name)
    return ok


def load_local_env(path):
    d = {}
    for line in open(path):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            d[k] = v
    return d


def read_remote(ssh, path):
    sftp = ssh.open_sftp()
    with sftp.open(path, "r") as f:
        data = f.read().decode()
    sftp.close()
    return data


def write_remote(ssh, path, data, mode=None):
    sftp = ssh.open_sftp()
    with sftp.open(path, "w") as f:
        f.write(data)
    if mode:
        sftp.chmod(path, mode)
    sftp.close()


def upsert_env(text, key, value):
    if re.search(rf"^{re.escape(key)}=", text, flags=re.M):
        return text, False
    return text.rstrip("\n") + f"\n{key}={value}\n", True


def main():
    zoho = load_local_env(f"{L}/zoho-oauth.env")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username="root", key_filename=PEM, timeout=25)
    print(f"connected to {HOST}")

    # ---------------- phase 0: env secrets ----------------
    code, o, _ = run(ssh, f"cat {REMOTE['backend_env']}")
    backend_env = o
    code, o, _ = run(ssh, f"cat {REMOTE['receiver_env']}")
    receiver_env = o

    m = re.search(r"^INTERNAL_PROVISION_SECRET=(.+)$", backend_env, flags=re.M)
    secret = m.group(1).strip() if m else pysecrets.token_urlsafe(32)

    backend_env, a1 = upsert_env(backend_env, "INTERNAL_PROVISION_SECRET", secret)
    backend_env, a2 = upsert_env(backend_env, "PUBLIC_APP_ORIGIN", "https://denialsdoctor.com")
    receiver_env, a3 = upsert_env(receiver_env, "BACKEND_INTERNAL_URL", "http://127.0.0.1:8000")
    receiver_env, a4 = upsert_env(receiver_env, "INTERNAL_PROVISION_SECRET", secret)
    receiver_env, a5 = upsert_env(receiver_env, "ADMIN_NOTIFY_EMAIL", "rajesh@ariaagent.agency")
    receiver_env, a6 = upsert_env(receiver_env, "MAIL_FROM_ADDRESS", "rajesh@ariaagent.agency")
    receiver_env, a7 = upsert_env(receiver_env, "MAIL_FROM_NAME", "DenialsDoctor")
    receiver_env, a8 = upsert_env(receiver_env, "ZOHO_CLIENT_ID", zoho["ZOHO_CLIENT_ID"])
    receiver_env, a9 = upsert_env(receiver_env, "ZOHO_CLIENT_SECRET", zoho["ZOHO_CLIENT_SECRET"])
    receiver_env, a10 = upsert_env(receiver_env, "ZOHO_REFRESH_TOKEN", zoho["ZOHO_REFRESH_TOKEN"])
    receiver_env, a11 = upsert_env(receiver_env, "ZOHO_ACCOUNT_ID", "5239518000000002002")
    receiver_env, a12 = upsert_env(receiver_env, "ZOHO_TOKEN_URL", "https://accounts.zoho.in/oauth/v2/token")
    receiver_env, a13 = upsert_env(receiver_env, "PROVISION_TEST_EVENTS", "0")

    write_remote(ssh, REMOTE["backend_env"], backend_env, mode=0o600)
    write_remote(ssh, REMOTE["receiver_env"], receiver_env, mode=0o600)
    step("phase0 env secrets", True, f"added {sum([a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13])} new keys")

    # ---------------- phase 1: backend ----------------
    sftp = ssh.open_sftp()
    sftp.put(LOCAL["provisioning"], REMOTE["provisioning"])
    sftp.close()
    step("upload provisioning.py", True)

    server_src = read_remote(ssh, REMOTE["server"])
    run(ssh, f"cp {REMOTE['server']} {REMOTE['server']}.bak.fulfill.{TS}")
    patched = server_src

    if "provisioning_router" not in patched:
        anchor = "from .hipaa_router import router as hipaa_router"
        patched = patched.replace(
            anchor,
            "from .provisioning import router as provisioning_router\n" + anchor, 1)
        patched = patched.replace(
            "app.include_router(public_tools_router)",
            "app.include_router(provisioning_router)\napp.include_router(public_tools_router)", 1)
        step("server.py router hook", "provisioning_router" in patched)
    else:
        step("server.py router hook", True, "already present")

    me_old = '''    return {
        "user_id": session.user_id,
        "email": session.email,
        "role": session.role,
        "client_id": session.client_id,
    }'''
    me_new = '''    client_rec = service.get_client(session.client_id)
    return {
        "user_id": session.user_id,
        "email": session.email,
        "role": session.role,
        "client_id": session.client_id,
        "plan": (client_rec or {}).get("plan"),
        "company": (client_rec or {}).get("name"),
    }'''
    if '"plan": (client_rec' not in patched:
        if me_old in patched:
            patched = patched.replace(me_old, me_new, 1)
        step("server.py /auth/me plan field", '"plan": (client_rec' in patched)
    else:
        step("server.py /auth/me plan field", True, "already present")

    import ast
    try:
        ast.parse(patched)
        write_remote(ssh, REMOTE["server"], patched)
        step("server.py AST check + upload", True)
    except SyntaxError as e:
        step("server.py AST check + upload", False, str(e))
        print("ABORTING: server.py patch failed validation; original untouched")
        ssh.close()
        sys.exit(1)

    code, o, e = run(ssh, "systemctl restart denials-doctor && sleep 4 && curl -s -m 10 http://127.0.0.1:8000/health")
    ok = code == 0 and '"status"' in o and '"ok"' in o
    if not ok:
        step("backend restart + health", False, (o + e)[:300])
        run(ssh, f"cp {REMOTE['server']}.bak.fulfill.{TS} {REMOTE['server']} && systemctl restart denials-doctor")
        print("ROLLED BACK backend; aborting")
        ssh.close()
        sys.exit(1)
    step("backend restart + health", True)

    code, o, _ = run(ssh, "curl -s -m 10 -X POST http://127.0.0.1:8000/internal/provision -H 'Content-Type: application/json' -d '{}' -o /dev/null -w '%{http_code}'")
    step("internal/provision mounted (403 without secret expected)", o.strip() == "403", f"got {o.strip()}")

    # ---------------- phase 2: receiver ----------------
    run(ssh, f"cp {REMOTE['receiver']} {REMOTE['receiver']}.bak.fulfill.{TS}")
    write_remote(ssh, REMOTE["receiver"], open(LOCAL["receiver"]).read())
    code, o, e = run(ssh, "python3 -m py_compile /opt/dd-dodo-webhook/receiver.py")
    okc = step("receiver syntax check", code == 0, (o + e)[:200])
    code, o, e = run(ssh, "systemctl restart dd-dodo-webhook && sleep 2 && curl -s -m 10 http://127.0.0.1:8787/api/webhooks/dodo/health")
    okr = code == 0 and '"ok": true' in o
    if not okr:
        step("receiver restart + health", False, (o + e)[:300])
        run(ssh, f"cp {REMOTE['receiver']}.bak.fulfill.{TS} {REMOTE['receiver']} && systemctl restart dd-dodo-webhook")
        print("ROLLED BACK receiver; continuing to static phases")
    else:
        step("receiver restart + health", True)

    # ---------------- phase 3: static pages ----------------
    sftp = ssh.open_sftp()
    try:
        sftp.mkdir(f"{REMOTE['webroot']}/welcome")
    except IOError:
        pass
    sftp.close()
    for local, remote, name in [
        (LOCAL["welcome"], f"{REMOTE['webroot']}/welcome.html", "welcome.html"),
        (LOCAL["setpwd"], f"{REMOTE['webroot']}/welcome/set-password.html", "welcome/set-password.html"),
        (LOCAL["login"], f"{REMOTE['webroot']}/login.html", "login.html"),
        (LOCAL["console"], f"{REMOTE['webroot']}/console.html", "console.html"),
    ]:
        sftp = ssh.open_sftp()
        sftp.put(local, remote)
        sftp.close()
        step(f"upload {name}", True)

    run(ssh, f"cp {REMOTE['start']} {REMOTE['start']}.bak.fulfill.{TS}")
    code, o, _ = run(ssh,
        "sed -i 's|redirect_url=https%3A%2F%2Fdenialsdoctor.com\"|redirect_url=https%3A%2F%2Fdenialsdoctor.com%2Fwelcome\"|g' "
        + REMOTE["start"] + f" && grep -c 'redirect_url=https%3A%2F%2Fdenialsdoctor.com%2Fwelcome' {REMOTE['start']}")
    step("start.html redirects → /welcome", code == 0 and o.strip() == "3", f"count={o.strip()}")

    sm = read_remote(ssh, REMOTE["sitemap"])
    if "/welcome<" not in sm and "denialsdoctor.com/welcome" not in sm:
        sm = sm.replace("</urlset>",
            "  <url><loc>https://denialsdoctor.com/welcome</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>")
        write_remote(ssh, REMOTE["sitemap"], sm)
        step("sitemap.xml + /welcome", "denialsdoctor.com/welcome" in sm)
    else:
        step("sitemap.xml + /welcome", True, "already present")

    # ---------------- phase 4: caddy ----------------
    run(ssh, f"cp {REMOTE['caddy']} /etc/caddy/Caddyfile.bak.fulfill.{TS}")
    caddy = read_remote(ssh, REMOTE["caddy"])

    if "/welcome/set-password" not in caddy:
        caddy = caddy.replace(
            "/sitemap.xml /agents /agents/*",
            "/sitemap.xml /welcome /welcome/set-password /login /app /agents /agents/*", 1)

    handles = """
		@welcomePage path /welcome
		handle @welcomePage {
			rewrite * /welcome.html
		}
		@setPwdPage path /welcome/set-password
		handle @setPwdPage {
			rewrite * /welcome/set-password.html
		}
		@loginPage path /login
		handle @loginPage {
			rewrite * /login.html
			header Cache-Control "no-store, no-cache, must-revalidate"
		}
		@appPage path /app
		handle @appPage {
			rewrite * /console.html
			header Cache-Control "no-store, no-cache, must-revalidate"
		}

		file_server
	}"""
    if "@welcomePage" not in caddy:
        anchor = """		@investorsPage path /investors
		handle @investorsPage {
			rewrite * /investor-deck.html
		}

		file_server
	}"""
        if anchor in caddy:
            caddy = caddy.replace(anchor, handles, 1)
            step("caddy rewrite handles inserted", "@welcomePage" in caddy)
        else:
            step("caddy rewrite handles inserted", False, "anchor not found")
    else:
        step("caddy rewrite handles inserted", True, "already present")

    if "reverse_proxy 127.0.0.1:8001" in caddy:
        caddy = caddy.replace("reverse_proxy 127.0.0.1:8001", "reverse_proxy 127.0.0.1:3100")
        step("agents. vhost → port 3100", "reverse_proxy 127.0.0.1:3100" in caddy)
    else:
        step("agents. vhost → port 3100", True, "already fixed")

    # lockdown: /internal/* must never be reachable through api. vhost
    if "handle /internal/*" not in caddy:
        caddy = caddy.replace("""# API endpoint (FastAPI v3.7 backend)
api.denialsdoctor.com {
	encode gzip zstd
""", """# API endpoint (FastAPI v3.7 backend)
api.denialsdoctor.com {
	encode gzip zstd

	# provisioning bridge: loopback-only (receiver calls 127.0.0.1:8000 directly)
	handle /internal/* {
		respond 404
	}
""", 1)
        step("caddy /internal lockdown", "handle /internal/*" in caddy)
    else:
        step("caddy /internal lockdown", True, "already present")

    write_remote(ssh, REMOTE["caddy"], caddy)
    code, o, e = run(ssh, "caddy validate --config /etc/caddy/Caddyfile 2>&1 | tail -2")
    if code == 0 and "Valid configuration" in o:
        run(ssh, "systemctl reload caddy")
        step("caddy validate + reload", True)
    else:
        run(ssh, f"cp /etc/caddy/Caddyfile.bak.fulfill.{TS} /etc/caddy/Caddyfile && systemctl reload caddy")
        step("caddy validate + reload", False, (o + e)[:200] + " — backup restored")

    # ---------------- public verification ----------------
    checks = [
        ("https://denialsdoctor.com/welcome", "trial has started"),
        ("https://denialsdoctor.com/welcome/set-password?token=x", "Set your password"),
        ("https://denialsdoctor.com/login", "Sign in to your workspace"),
        ("https://denialsdoctor.com/app", "Denial Desk"),
        ("https://denialsdoctor.com/api/webhooks/dodo/health", "ok"),
        ("https://denialsdoctor.com/start", "checkout.dodopayments.com"),
    ]
    for url, expect in checks:
        code, o, _ = run(ssh, f"curl -s -m 15 '{url}' | grep -c '{expect}'")
        step(f"public {url}", code == 0 and int(o.strip() or 0) > 0, f"matches={o.strip()}")

    code, o, _ = run(ssh, "curl -s -o /dev/null -w '%{http_code}' -m 15 https://denialsdoctor.com/api/webhooks/dodo/health")
    step("webhook public health 200", o.strip() == "200", o.strip())

    code, o, _ = run(ssh, "curl -s -o /dev/null -w '%{http_code}' -m 15 https://api.denialsdoctor.com/internal/provision -X POST")
    step("api. /internal lockdown 404", o.strip() == "404", o.strip())

    print()
    print("RESULT:", "ALL OK" if not failures else f"FAILURES: {failures}")
    ssh.close()


if __name__ == "__main__":
    main()
