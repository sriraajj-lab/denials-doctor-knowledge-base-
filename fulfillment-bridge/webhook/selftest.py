#!/usr/bin/env python3
"""Self-test for dd-dodo-webhook receiver. Run on prod server as root."""
import base64
import hashlib
import hmac
import json
import time
import urllib.request
import urllib.error

BASE = "http://127.0.0.1:8787"
SECRET = ""
ADMIN_TOKEN = ""
for line in open("/etc/dd-dodo-webhook/env"):
    line = line.strip()
    if line.startswith("DODO_WEBHOOK_KEY="):
        SECRET = line.split("=", 1)[1].strip()
    if line.startswith("ADMIN_TOKEN="):
        ADMIN_TOKEN = line.split("=", 1)[1].strip()

if not SECRET:
    raise SystemExit("no secret configured")


def sign(payload, wh_id, ts):
    secret_bytes = base64.b64decode(SECRET[len("whsec_"):])
    mac = hmac.new(secret_bytes, f"{wh_id}.{ts}.{payload}".encode(), hashlib.sha256).digest()
    return "v1," + base64.b64encode(mac).decode()


def post(payload, signed=True, bad_sig=False, wh_id=None, raw_body=None):
    body = raw_body if raw_body is not None else json.dumps(payload)
    wh_id = wh_id or f"msg_test_{int(time.time() * 1000):x}"
    ts = str(int(time.time()))
    headers = {"Content-Type": "application/json"}
    if signed:
        sig = sign(body, wh_id, ts)
        if bad_sig:
            sig = "v1," + "A" * 44
        headers["webhook-id"] = wh_id
        headers["webhook-timestamp"] = ts
        headers["webhook-signature"] = sig
    req = urllib.request.Request(f"{BASE}/api/webhooks/dodo", data=body.encode(),
                                 headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def get(path):
    try:
        with urllib.request.urlopen(f"{BASE}{path}", timeout=10) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


EVENT = {
    "id": "evt_selftest_001",
    "type": "subscription.active",
    "timestamp": "2026-10-29T19:40:00Z",
    "data": {"object": {
        "id": "sub_test_selftest001",
        "subscription_id": "sub_test_selftest001",
        "status": "active",
        "customer": "cus_test_selftest001",
        "product_id": "pdt_0NqnxnwDT8ho2QhJDDErG",
        "customer_email": "selftest+webhook@denialsdoctor.com",
        "metadata": {"test": "true"},
    }},
}

CANCEL = {
    "id": "evt_selftest_002",
    "type": "subscription.cancelled",
    "timestamp": "2026-10-29T19:45:00Z",
    "data": {"object": {
        "id": "sub_test_selftest001",
        "subscription_id": "sub_test_selftest001",
        "status": "cancelled",
        "customer": "cus_test_selftest001",
        "product_id": "pdt_0NqnxnwDT8ho2QhJDDErG",
        "customer_email": "selftest+webhook@denialsdoctor.com",
        "metadata": {"test": "true"},
    }},
}

fails = 0


def check(label, got, want):
    global fails
    ok = got == want
    print(f"[{'OK' if ok else 'FAIL'}] {label}: got {got}, want {want}")
    if not ok:
        fails += 1


s, b = post(EVENT, signed=False)
check("unsigned rejected", s, 401)

s, b = post(EVENT, signed=True, bad_sig=True)
check("bad signature rejected", s, 403)

s, b = post(EVENT)
check("valid event accepted", s, 200)
print("      response:", b)

s, b = post(EVENT, wh_id=None)
# second send of same event id -> duplicate
check("second event accepted", s, 200)

# duplicate delivery: Dodo retries reuse the SAME webhook id -> second copy is a dup
body = json.dumps(EVENT)
ts = str(int(time.time()))
wh_id = f"msg_dup_{int(time.time() * 1000):x}"
sig = sign(body, wh_id, ts)
hdrs = {"Content-Type": "application/json", "webhook-id": wh_id,
        "webhook-timestamp": ts, "webhook-signature": sig}


def post_dup():
    req = urllib.request.Request(
        f"{BASE}/api/webhooks/dodo", data=body.encode(), method="POST", headers=hdrs)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


post_dup()                                  # first delivery -> processed
d = post_dup()                              # retry with same id -> idempotent
check("duplicate id -> idempotent", d.get("duplicate"), True)

s, b = post(CANCEL)
check("cancel event accepted", s, 200)

s, b = get("/api/webhooks/dodo/health")
check("health", s, 200)

s, b = get("/api/webhooks/dodo/admin")
check("admin without token forbidden", s, 403)

s, b = get(f"/api/webhooks/dodo/admin?token={ADMIN_TOKEN}")
check("admin with token", s, 200)
subs = b.get("subscriptions", {})
ent = b.get("entitlements", {})
print("\n-- subscriptions --"); print(json.dumps(subs, indent=2)[:1200])
print("\n-- entitlements --"); print(json.dumps(ent, indent=2)[:800])
check("sub recorded", subs.get("sub_test_selftest001", {}).get("status"), "cancelled")
check("entitlement revoked after cancel",
      ent.get("selftest+webhook@denialsdoctor.com", {}).get("access"), "revoked")

print(f"\n{'ALL TESTS PASSED' if fails == 0 else f'{fails} FAILURES'}")
raise SystemExit(0 if fails == 0 else 1)
