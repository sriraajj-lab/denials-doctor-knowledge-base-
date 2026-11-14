#!/usr/bin/env python3
"""E2E verification of the DenialsDoctor fulfillment bridge (runs ON the droplet).

Chain under test:
  1. POST /internal/provision (with secret) -> client + user + token
  2. GET  /auth/set-password/verify?token   -> valid + email
  3. POST /auth/set-password                -> ok
  4. POST /auth/login                       -> session token
  5. GET  /auth/me                          -> plan reflects the bought tier
  6. POST /internal/provision without secret -> 403
Cleanup: soft-deletes the QA client/user rows at the end (keeps audit trail).
"""
import json
import secrets
import sqlite3
import sys
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8000"
SECRET = None
DB = "/var/lib/denials-doctor/outcomes.db"

for line in open("/etc/denials-doctor/env"):
    if line.startswith("INTERNAL_PROVISION_SECRET="):
        SECRET = line.strip().split("=", 1)[1]
assert SECRET, "secret not found in env"


def req(path, payload=None, headers=None, method=None):
    data = json.dumps(payload).encode() if payload is not None else None
    h = {"Content-Type": "application/json"}
    h.update(headers or {})
    r = urllib.request.Request(BASE + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}


def cleanup(client_id):
    conn = sqlite3.connect(DB, timeout=10)
    now = "2026-11-13T00:00:00Z"
    conn.execute("UPDATE users SET status='deleted', deleted_at=? WHERE client_id=?", (now, client_id))
    conn.execute("UPDATE clients SET status='deleted', deleted_at=? WHERE id=?", (now, client_id))
    conn.commit()
    n_u = conn.execute("SELECT changes()").fetchone()[0]
    conn.close()
    print(f"CLEANUP: soft-deleted client {client_id} (users affected: {n_u})")


def main():
    results = []
    qa_email = f"qa.e2e.{secrets.token_hex(4)}@denialsdoctor.com"
    print(f"QA buyer identity: {qa_email}")

    # 6. security first: no secret -> 403
    st, _ = req("/internal/provision", {"email": qa_email, "plan": "starter"})
    results.append(("provision without secret -> 403", st == 403, st))

    # 1. provision
    st, d = req("/internal/provision", {
        "email": qa_email, "plan": "starter",
        "company_name": "QA E2E Practice",
        "product_id": "pdt_0NqnxnPUHZXKgQ77a08gz",
        "subscription_id": "sub_qa_e2e_" + secrets.token_hex(4),
    }, headers={"X-Internal-Secret": SECRET})
    ok1 = st == 200 and d.get("created_client") and d.get("created_user") and d.get("password_token")
    results.append(("provision creates client+user+token", ok1, st))
    client_id = d.get("client_id")
    token = d.get("password_token")
    url = d.get("set_password_url") or ""
    print("  client:", client_id, "| token issued:", bool(token), "| url host ok:", "denialsdoctor.com/welcome/set-password?token=" in url)

    # 2. verify token
    st, d = req("/auth/set-password/verify?token=" + urllib.request.quote(token))
    results.append(("verify token valid + email", st == 200 and d.get("valid") and d.get("email") == qa_email, d))

    # 3. set password
    pw = "Qa-E2E-" + secrets.token_hex(8)
    st, d = req("/auth/set-password", {"token": token, "password": pw})
    results.append(("set-password -> ok", st == 200 and d.get("status") == "ok", st))

    # token single-use check
    st, d = req("/auth/set-password", {"token": token, "password": pw + "x"})
    results.append(("token is single-use (400 on reuse)", st == 400, st))

    # 4. login
    st, d = req("/auth/login", {"email": qa_email, "password": pw})
    tok = d.get("token")
    results.append(("login with new password", st == 200 and bool(tok), st))

    # 5. me -> plan
    st, d = req("/auth/me", headers={"Authorization": "Bearer " + tok})
    results.append(("/auth/me shows plan=starter", st == 200 and d.get("plan") == "starter", d.get("plan")))

    # re-provision idempotency (renewal path): no new client/user, no new token
    st, d = req("/internal/provision", {
        "email": qa_email, "plan": "starter", "subscription_id": "sub_qa_renew",
    }, headers={"X-Internal-Secret": SECRET})
    results.append(("re-provision idempotent (no token, existing active user)",
                    st == 200 and not d.get("created_user") and d.get("note") == "existing-active-user-no-token", d.get("note")))

    print()
    failed = [r for r in results if not r[1]]
    for name, ok, detail in results:
        print(("✓" if ok else "✗") + " " + name + ("" if ok else f"  ({detail})"))
    cleanup(client_id)
    print("RESULT:", "ALL OK" if not failed else f"FAILED: {[f[0] for f in failed]}")


if __name__ == "__main__":
    main()
