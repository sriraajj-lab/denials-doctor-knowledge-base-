#!/usr/bin/env python3
"""Webhook-chain test: signed granted event -> receiver -> provision + emails.

Run steps (this script does all):
  1. enable PROVISION_TEST_EVENTS=1, restart receiver
  2. send ONE signed subscription.active (Starter, test=true) via public route
  3. read journalctl for the fulfill line; check entitlements + provisioning log
  4. restore PROVISION_TEST_EVENTS=0, restart receiver
  5. soft-delete the QA client/user created by the event
Run ON the droplet as root.
"""
import json
import base64
import hashlib
import hmac
import sqlite3
import subprocess
import time
import urllib.request

BASE = "http://127.0.0.1:8787"
DB = "/var/lib/denials-doctor/outcomes.db"
QA_EMAIL = "selftest+fulfill@denialsdoctor.com"
NOW = int(time.time())


def sh(cmd, timeout=60):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def env_set(value):
    sh(f"sed -i 's/^PROVISION_TEST_EVENTS=.*/PROVISION_TEST_EVENTS={value}/' /etc/dd-dodo-webhook/env")
    sh("systemctl restart dd-dodo-webhook && sleep 2")
    code, o, _ = sh("curl -s -m 8 http://127.0.0.1:8787/api/webhooks/dodo/health")
    return '"ok": true' in o


def sign_and_post():
    secret = ""
    for line in open("/etc/dd-dodo-webhook/env"):
        if line.startswith("DODO_WEBHOOK_KEY="):
            secret = line.strip().split("=", 1)[1]
    sb = base64.b64decode(secret[len("whsec_"):])
    wh_id = f"msg_fulfille2e_{NOW:x}"
    ts = str(NOW)
    payload = {
        "type": "subscription.active",
        "data": {"object": {
            "id": f"sub_fulfille2e_{NOW:x}",
            "subscription_id": f"sub_fulfille2e_{NOW:x}",
            "status": "active",
            "customer": f"cus_fulfille2e_{NOW:x}",
            "customer_email": QA_EMAIL,
            "product_id": "pdt_0NqnxnPUHZXKgQ77a08gz",
            "metadata": {"test": "true"},
        }},
    }
    body = json.dumps(payload)
    sig = "v1," + base64.b64encode(
        hmac.new(sb, f"{wh_id}.{ts}.{body}".encode(), hashlib.sha256).digest()).decode()
    req = urllib.request.Request(BASE + "/api/webhooks/dodo", data=body.encode(), headers={
        "Content-Type": "application/json",
        "webhook-id": wh_id,
        "webhook-timestamp": ts,
        "webhook-signature": sig,
    }, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status, json.loads(r.read().decode())


def main():
    results = []

    ok = env_set(1)
    results.append(("enable PROVISION_TEST_EVENTS + receiver healthy", ok))

    st, d = sign_and_post()
    results.append(("signed event accepted via receiver", st == 200 and d.get("received"), (st, d)))
    time.sleep(3)  # give fulfill() time to call backend + Zoho

    code, j, _ = sh("journalctl -u dd-dodo-webhook --since '-2 min' --no-pager | grep fulfill | tail -5")
    print("journal:", j or "(no fulfill lines)")
    results.append(("fulfill ran with provision + mail results", "provision=ok" in j, j))

    code, o, _ = sh("grep -c 'fulfill' /var/lib/dd-dodo-webhook/events.jsonl || true")
    ent = json.load(open("/var/lib/dd-dodo-webhook/entitlements.json"))
    granted = [k for k, v in ent.items() if v.get("access") == "granted" and "fulfill" in k]
    results.append(("entitlements granted for QA email", len(granted) == 1, granted))

    # backend actually created the account?
    conn = sqlite3.connect(DB, timeout=10)
    row = conn.execute("SELECT u.id, u.client_id, u.role, c.plan FROM users u JOIN clients c ON c.id=u.client_id WHERE u.email=? AND u.deleted_at IS NULL", (QA_EMAIL,)).fetchone()
    conn.close()
    results.append(("backend account created for webhook buyer", row is not None and row[3] == "starter", row))

    ok = env_set(0)
    results.append(("restore PROVISION_TEST_EVENTS=0 + healthy", ok))

    if row:
        conn = sqlite3.connect(DB, timeout=10)
        conn.execute("UPDATE users SET status='deleted', deleted_at=datetime('now') WHERE email=?", (QA_EMAIL,))
        conn.execute("UPDATE clients SET status='deleted', deleted_at=datetime('now') WHERE id=?", (row[1],))
        conn.commit()
        conn.close()
        print("cleanup: soft-deleted", row[1])

    print()
    for name, ok, detail in results:
        print(("✓" if ok else "✗") + " " + name + ("" if ok else f"  ({detail})"))
    print("RESULT:", "ALL OK" if all(r[1] for r in results) else "FAILURES ABOVE")


if __name__ == "__main__":
    main()
