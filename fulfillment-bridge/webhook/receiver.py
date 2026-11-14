#!/usr/bin/env python3
"""
DenialsDoctor — Dodo Payments webhook receiver.

Standard Webhooks verification (matches Dodo/Aria pattern):
  headers: webhook-id, webhook-timestamp, webhook-signature: "v1,<b64 hmac>"
  signed_content = "{id}.{timestamp}.{raw_body}"
  HMAC-SHA256 keyed with base64-decoded bytes of whsec_ secret.

State (under STATE_DIR):
  events.jsonl       — append-only audit of every verified event
  subscriptions.json — latest known state per subscription
  entitlements.json  — derived access map per customer (granted/grace/revoked)

Endpoints (behind Caddy on denialsdoctor.com):
  POST /api/webhooks/dodo          — Dodo delivery target
  GET  /api/webhooks/dodo/health   — liveness
  GET  /api/webhooks/dodo/admin    — state snapshot (requires token)
"""
import base64
import hashlib
import hmac
import json
import os
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

LISTEN_HOST = os.environ.get("LISTEN_HOST", "127.0.0.1")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", "8787"))
SECRET = os.environ.get("DODO_WEBHOOK_KEY", "").strip()
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "").strip()

# ---- Fulfillment bridge (v1.1): provision + welcome email + admin notify ----
BACKEND_URL = os.environ.get("BACKEND_INTERNAL_URL", "http://127.0.0.1:8000").rstrip("/")
PROVISION_SECRET = os.environ.get("INTERNAL_PROVISION_SECRET", "").strip()
ADMIN_NOTIFY_EMAIL = os.environ.get("ADMIN_NOTIFY_EMAIL", "").strip()
MAIL_FROM = os.environ.get("MAIL_FROM_ADDRESS", "rajesh@ariaagent.agency").strip()
MAIL_FROM_NAME = os.environ.get("MAIL_FROM_NAME", "DenialsDoctor").strip()
ZOHO_CLIENT_ID = os.environ.get("ZOHO_CLIENT_ID", "").strip()
ZOHO_CLIENT_SECRET = os.environ.get("ZOHO_CLIENT_SECRET", "").strip()
ZOHO_REFRESH_TOKEN = os.environ.get("ZOHO_REFRESH_TOKEN", "").strip()
ZOHO_ACCOUNT_ID = os.environ.get("ZOHO_ACCOUNT_ID", "").strip()
ZOHO_TOKEN_URL = os.environ.get("ZOHO_TOKEN_URL", "https://accounts.zoho.in/oauth/v2/token")
ZOHO_SEND_URL = os.environ.get(
    "ZOHO_SEND_URL", f"https://mail.zoho.in/api/accounts/{ZOHO_ACCOUNT_ID}/messages").strip()
PROVISION_TEST_EVENTS = os.environ.get("PROVISION_TEST_EVENTS", "0") == "1"
# Aria Managed plans are services, not SaaS logins: no account provisioning,
# but the buyer still gets an onboarding-contact email (any plan not in
# PLAN_TO_TIER is treated as managed).
PLAN_TO_TIER = {"Starter": "starter", "Professional": "pro", "Enterprise": "enterprise"}

STATE_DIR = Path(os.environ.get("STATE_DIR", "/var/lib/dd-dodo-webhook"))
EVENTS_LOG = STATE_DIR / "events.jsonl"
SUBS_FILE = STATE_DIR / "subscriptions.json"
ENTITLE_FILE = STATE_DIR / "entitlements.json"
MAX_AGE_SEC = 300
MAX_BODY = 1_000_000
MAX_PAYLOAD_KEEP = 8 * 1024

PRODUCT_MAP = {
    "pdt_0NqnxnPUHZXKgQ77a08gz": {"plan": "Starter", "price_usd": 99, "line": "DenialsDoctor SaaS"},
    "pdt_0NqnxnwDT8ho2QhJDDErG": {"plan": "Professional", "price_usd": 299, "line": "DenialsDoctor SaaS"},
    "pdt_0NqnxoS83AEidEtvLTYF5": {"plan": "Enterprise", "price_usd": 799, "line": "DenialsDoctor SaaS"},
    "pdt_0Nqfb9zyQ5tLYHUsktWq3": {"plan": "Aria Managed Starter", "price_usd": 497, "line": "Aria Managed"},
    "pdt_0NqfbA4GM3rjYjXQ23vRC": {"plan": "Aria Managed Business", "price_usd": 997, "line": "Aria Managed"},
    "pdt_0NqfbA8qPoRR5Slus9MSO": {"plan": "Aria Managed Office Max", "price_usd": 1997, "line": "Aria Managed"},
}
GRANT = {"active", "on_trial"}
GRACE = {"on_hold", "past_due", "payment_failed", "paused", "incomplete"}
REVOKE = {"cancelled", "expired", "failed", "incomplete_expired"}

_lock = threading.Lock()
_seen_ids = set()


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path, default):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return default


def save_json(path, data):
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, default=str))
    tmp.replace(path)


def find_emails(obj):
    """Recursively collect values of keys named 'email' or '*_email'."""
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and ("email" in k.lower()) and "@" in v:
                out.append(v.strip().lower())
            else:
                out.extend(find_emails(v))
    elif isinstance(obj, list):
        for item in obj:
            out.extend(find_emails(item))
    return out


def derive_access(status):
    s = (status or "").strip().lower()
    if s in GRANT:
        return "granted"
    if s in GRACE:
        return "grace"
    if s in REVOKE:
        return "revoked"
    return "unknown:" + (s or "none")


# ---------------------------------------------------------------------------
# Fulfillment bridge (v1.1)
# ---------------------------------------------------------------------------

_zoho_token_cache = {"access_token": None, "expires_at": 0.0}


def _http_json(url, payload=None, headers=None, method=None, timeout=20):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, json.loads(resp.read().decode())


def _zoho_access_token():
    if _zoho_token_cache["access_token"] and time.time() < _zoho_token_cache["expires_at"]:
        return _zoho_token_cache["access_token"]
    if not (ZOHO_CLIENT_ID and ZOHO_CLIENT_SECRET and ZOHO_REFRESH_TOKEN):
        return None
    body = urllib.parse.urlencode({
        "refresh_token": ZOHO_REFRESH_TOKEN,
        "client_id": ZOHO_CLIENT_ID,
        "client_secret": ZOHO_CLIENT_SECRET,
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(ZOHO_TOKEN_URL, data=body)
    with urllib.request.urlopen(req, timeout=20) as resp:
        tok = json.loads(resp.read().decode())
    _zoho_token_cache["access_token"] = tok.get("access_token")
    _zoho_token_cache["expires_at"] = time.time() + int(tok.get("expires_in", 3600)) - 120
    return _zoho_token_cache["access_token"]


def zoho_send(to, subject, html):
    at = _zoho_access_token()
    if not at or not ZOHO_ACCOUNT_ID:
        return "mail-not-configured"
    payload = {
        "fromAddress": MAIL_FROM,
        "toAddress": to,
        "subject": subject,
        "content": html,
        "mailFormat": "html",
        "askReceipt": "no",
    }
    status, _ = _http_json(
        ZOHO_SEND_URL, payload=payload,
        headers={"Authorization": f"Zoho-oauthtoken {at}",
                 "Content-Type": "application/json"},
        method="POST",
    )
    return "ok" if status in (200, 201) else f"http-{status}"


def backend_provision(email, tier, product_id, sub_id, customer_id):
    if not PROVISION_SECRET:
        return None, "provision-secret-not-configured"
    payload = {
        "email": email,
        "plan": tier,
        "product_id": product_id,
        "subscription_id": sub_id,
        "customer_id": customer_id,
        "source": "dodo-webhook",
    }
    try:
        status, data = _http_json(
            f"{BACKEND_URL}/internal/provision", payload=payload,
            headers={"X-Internal-Secret": PROVISION_SECRET,
                     "Content-Type": "application/json"},
            method="POST",
        )
        if status == 200:
            return data, "ok"
        return None, f"http-{status}:{data}"
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def _email_shell(title, body_html, cta_url=None, cta_label=None):
    cta = ""
    if cta_url and cta_label:
        cta = (f'<p style="margin:26px 0 10px"><a href="{cta_url}" '
               f'style="background:#10b981;color:#ffffff;padding:13px 26px;'
               f'border-radius:9px;text-decoration:none;font-weight:700;'
               f'display:inline-block">{cta_label}</a></p>'
               f'<p style="color:#71717a;font-size:12px">Or copy this link: {cta_url}</p>')
    return f"""<!doctype html><html><body style="margin:0;background:#f4f4f5;font-family:Segoe UI,Roboto,Helvetica,Arial,sans-serif">
<div style="max-width:560px;margin:0 auto;background:#ffffff;border:1px solid #e4e4e7;border-radius:12px;overflow:hidden">
<div style="background:#09090b;padding:18px 26px"><span style="color:#fafafa;font-weight:800;font-size:17px">Denials<b style="color:#10b981">Doctor</b></span></div>
<div style="padding:26px">
<h2 style="margin:0 0 12px;color:#18181b;font-size:20px">{title}</h2>
{body_html}
{cta}
<p style="margin-top:26px;color:#a1a1aa;font-size:12px">DenialsDoctor · denialsdoctor.com · Questions? Reply to this email — a human reads it.</p>
</div></div></body></html>"""


def _welcome_email_html(email, set_password_url, plan):
    body = (f"<p style='color:#3f3f46;font-size:14px;line-height:1.6'>Welcome aboard — your "
            f"<b>DenialsDoctor {plan}</b> 15-day free trial is active.</p>"
            "<p style='color:#3f3f46;font-size:14px;line-height:1.6'>One step left before you can "
            "start recovering denied revenue: set your own password. It takes ten seconds and the "
            "link below works once.</p>"
            "<ol style='color:#3f3f46;font-size:14px;line-height:1.7;padding-left:18px'>"
            "<li>Click <b>Set my password</b> below and choose a password.</li>"
            "<li>Log in and open your dashboard.</li>"
            "<li>Add your first denied claim (CSV upload or manual entry) and run the denial "
            "analysis — most customers see their first appeal-ready letter within minutes.</li>"
            "</ol>"
            "<p style='color:#3f3f46;font-size:14px;line-height:1.6'>No account yet is also fine for "
            "our free tools: the <a href='https://denialsdoctor.com/appeal-letter-generator' "
            "style='color:#10b981'>Appeal Letter Generator</a> and the "
            "<a href='https://denialsdoctor.com/denial-code' style='color:#10b981'>Denial Code "
            "Lookup</a> work right now, no login needed.</p>")
    return _email_shell("Set your password to start using DenialsDoctor", body,
                        cta_url=set_password_url, cta_label="Set my password")


def _managed_email_html(email, plan):
    body = (f"<p style='color:#3f3f46;font-size:14px;line-height:1.6'>Thank you — your "
            f"<b>{plan}</b> subscription is confirmed.</p>"
            "<p style='color:#3f3f46;font-size:14px;line-height:1.6'>This is a done-for-you service, "
            "so there is nothing for you to set up. Your dedicated revenue-cycle team will reach out "
            "within one business day to collect your first batch of denied claims and walk you "
            "through what happens next.</p>"
            "<p style='color:#3f3f46;font-size:14px;line-height:1.6'>Meanwhile, the "
            "<a href='https://denialsdoctor.com/appeal-letter-generator' style='color:#10b981'>free "
            "Appeal Letter Generator</a> is yours to use right away.</p>")
    return _email_shell("You're in — here's what happens next", body)


def _admin_notify_html(row, provision_result, mail_result):
    import html as _h
    lines = "".join(
        f"<li>{_h.escape(str(k))}: {_h.escape(str(v))}</li>"
        for k, v in [
            ("Event", row.get("type")), ("Plan", row.get("plan")),
            ("Buyer", row.get("customer_email")), ("Subscription", row.get("subscription_id")),
            ("Product", row.get("product_id")), ("Test", row.get("test")),
            ("Provisioning", provision_result), ("Welcome email", mail_result),
        ])
    body = (f"<p style='color:#3f3f46;font-size:14px'>A new paid event was received and fulfilled "
            f"(or attempted):</p><ul style='color:#3f3f46;font-size:13px;line-height:1.7'>{lines}</ul>"
            "<p style='color:#3f3f46;font-size:14px'>If provisioning failed, re-run it manually: "
            "see the Fulfillment section of the operations handbook.</p>")
    return _email_shell("DenialsDoctor — new subscription event", body)


def fulfill(row):
    """Provision the buyer's account + send emails after a granted event.

    Never raises: any failure is logged on stdout (journalctl) and reported in
    the admin notification, so a broken mailer cannot break checkout.
    """
    try:
        email = row.get("customer_email")
        plan = row.get("plan")
        if row.get("access") != "granted" or not email or not plan:
            return
        if row.get("test") and not PROVISION_TEST_EVENTS:
            print(f"[{now_iso()}] fulfill: test event — skipped (PROVISION_TEST_EVENTS=0)", flush=True)
            return
        tier = PLAN_TO_TIER.get(plan)
        provision_result, mail_result = "-", "-"
        if tier:
            data, provision_result = backend_provision(
                email, tier, row.get("product_id"), row.get("subscription_id"),
                row.get("customer_id"),
            )
            set_url = (data or {}).get("set_password_url") if isinstance(data, dict) else None
            note = (data or {}).get("note") if isinstance(data, dict) else ""
            if note == "existing-active-user-no-token":
                mail_result = "skipped (user already active)"
            elif set_url:
                mail_result = zoho_send(email, "Set your password — DenialsDoctor trial active",
                                        _welcome_email_html(email, set_url, plan))
            else:
                mail_result = "no-token-from-provisioning"
        else:
            mail_result = zoho_send(email, "You're in — DenialsDoctor managed onboarding",
                                    _managed_email_html(email))
        if ADMIN_NOTIFY_EMAIL:
            zoho_send(ADMIN_NOTIFY_EMAIL, "[Fulfillment] new DenialsDoctor subscription event",
                      _admin_notify_html(row, provision_result, mail_result))
        print(f"[{now_iso()}] fulfill: {email} plan={plan} provision={provision_result} mail={mail_result}",
              flush=True)
    except Exception as e:
        print(f"[{now_iso()}] fulfill: ERROR {type(e).__name__}: {e}", flush=True)


def load_seen_ids():
    if not EVENTS_LOG.exists():
        return
    try:
        lines = EVENTS_LOG.read_text().splitlines()[-3000:]
        for ln in lines:
            try:
                _seen_ids.add(json.loads(ln).get("webhook_id"))
            except Exception:
                pass
    except Exception:
        pass


def process_event(wh_id, payload):
    ptype = payload.get("type") or "unknown"
    data = payload.get("data") or {}
    obj = data.get("object") if isinstance(data.get("object"), dict) else data

    obj_id = obj.get("id") or ""
    sub_id = obj.get("subscription_id") or (obj_id if "sub" in str(obj_id) else None)
    payment_id = obj.get("payment_id") or (obj_id if "pay" in str(obj_id) else None)
    customer_id = obj.get("customer") or data.get("customer")
    if isinstance(customer_id, dict):
        customer_id = customer_id.get("id")
    emails = find_emails(obj) or find_emails(data)
    email = emails[0] if emails else None

    product_id = obj.get("product_id")
    if not product_id and isinstance(obj.get("items"), list) and obj["items"]:
        first = obj["items"][0]
        product_id = first.get("product_id") or (first.get("price") or {}).get("product_id")
    meta = obj.get("metadata") or {}
    is_test = str(meta.get("test", "")).lower() == "true"
    plan_info = PRODUCT_MAP.get(product_id, {})

    row = {
        "received_at": now_iso(),
        "webhook_id": wh_id,
        "type": ptype,
        "subscription_id": sub_id,
        "payment_id": payment_id,
        "customer_id": customer_id,
        "customer_email": email,
        "product_id": product_id,
        "plan": plan_info.get("plan"),
        "status": obj.get("status"),
        "access": derive_access(obj.get("status")),
        "test": is_test,
    }

    with _lock:
        EVENTS_LOG.parent.mkdir(parents=True, exist_ok=True)
        keep = dict(row)
        try:
            blob = json.dumps(obj, default=str)
            if len(blob) > MAX_PAYLOAD_KEEP:
                blob = blob[:MAX_PAYLOAD_KEEP] + "...TRUNCATED"
                keep["object"] = blob
            else:
                keep["object"] = json.loads(blob)
        except Exception:
            pass
        with EVENTS_LOG.open("a") as f:
            f.write(json.dumps(keep, default=str) + "\n")

        if sub_id:
            subs = load_json(SUBS_FILE, {})
            entry = subs.get(sub_id) or {}
            entry.update({
                "subscription_id": sub_id,
                "status": obj.get("status") or entry.get("status"),
                "customer_id": customer_id or entry.get("customer_id"),
                "customer_email": email or entry.get("customer_email"),
                "product_id": product_id or entry.get("product_id"),
                "plan": plan_info.get("plan") or entry.get("plan"),
                "line": plan_info.get("line") or entry.get("line"),
                "price_usd": plan_info.get("price_usd") or entry.get("price_usd"),
                "last_event_type": ptype,
                "updated_at": now_iso(),
            })
            entry.setdefault("first_seen", now_iso())
            subs[sub_id] = entry
            save_json(SUBS_FILE, subs)

            ent = load_json(ENTITLE_FILE, {})
            key = email or customer_id or sub_id
            ent[key] = {
                "access": derive_access(obj.get("status")),
                "subscription_id": sub_id,
                "customer_id": customer_id,
                "customer_email": email,
                "plan": plan_info.get("plan") or entry.get("plan"),
                "status": obj.get("status"),
                "updated_at": now_iso(),
            }
            save_json(ENTITLE_FILE, ent)
    return row


def verify_signature(wh_id, wh_ts, wh_sig, body):
    if not (wh_id and wh_ts and wh_sig):
        return "missing-headers"
    try:
        ts = int(wh_ts)
    except ValueError:
        return "bad-timestamp"
    if abs(time.time() - ts) > MAX_AGE_SEC:
        return "expired-timestamp"
    if not SECRET:
        return "receiver-not-configured"
    secret_bytes = (
        base64.b64decode(SECRET[len("whsec_"):]) if SECRET.startswith("whsec_")
        else SECRET.encode()
    )
    signed_content = f"{wh_id}.{wh_ts}.{body}".encode()
    expected = base64.b64encode(
        hmac.new(secret_bytes, signed_content, hashlib.sha256).digest()
    ).decode()
    provided = [p.split(",", 1)[1] for p in wh_sig.split() if p.startswith("v1,")]
    if not provided:
        return "no-signature"
    if not any(hmac.compare_digest(expected, p) for p in provided):
        return "signature-mismatch"
    return None


class Handler(BaseHTTPRequestHandler):
    server_version = "dd-dodo-webhook/1.0"

    def _json(self, code, obj):
        blob = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(blob)))
        self.end_headers()
        self.wfile.write(blob)

    def do_POST(self):
        if self.path.rstrip("/") != "/api/webhooks/dodo":
            return self._json(404, {"error": "not-found"})
        if not SECRET:
            return self._json(503, {"error": "receiver-not-configured"})
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return self._json(400, {"error": "bad-content-length"})
        if length <= 0 or length > MAX_BODY:
            return self._json(400, {"error": "bad-body-size"})
        body = self.rfile.read(length).decode("utf-8", "replace")

        err = verify_signature(
            self.headers.get("webhook-id", ""),
            self.headers.get("webhook-timestamp", ""),
            self.headers.get("webhook-signature", ""),
            body,
        )
        if err == "missing-headers":
            return self._json(401, {"error": err})
        if err:
            return self._json(403, {"error": err})

        try:
            payload = json.loads(body)
        except Exception:
            return self._json(400, {"error": "invalid-json"})

        wh_id = self.headers.get("webhook-id", "")
        with _lock:
            dup = wh_id in _seen_ids
            if not dup:
                _seen_ids.add(wh_id)
        if dup:
            return self._json(200, {"received": True, "duplicate": True})
        row = process_event(wh_id, payload)
        fulfill(row)
        return self._json(200, {"received": True, "type": row["type"], "plan": row["plan"]})

    def do_GET(self):
        route, _, query = self.path.partition("?")
        if route.rstrip("/") == "/api/webhooks/dodo/health":
            return self._json(200, {"ok": True, "service": "dd-dodo-webhook",
                                    "secret_configured": bool(SECRET)})
        if route.rstrip("/") == "/api/webhooks/dodo/admin":
            params = urllib.parse.parse_qs(query)
            token = (params.get("token") or [""])[0]
            auth = self.headers.get("Authorization", "")
            if auth.startswith("Bearer ") and not token:
                token = auth[7:]
            if not ADMIN_TOKEN or not hmac.compare_digest(token, ADMIN_TOKEN):
                return self._json(403, {"error": "forbidden"})
            with _lock:
                subs = load_json(SUBS_FILE, {})
                ent = load_json(ENTITLE_FILE, {})
                recent = []
                if EVENTS_LOG.exists():
                    for ln in EVENTS_LOG.read_text().splitlines()[-20:]:
                        try:
                            e = json.loads(ln)
                            recent.append({k: e.get(k) for k in
                                           ("received_at", "type", "subscription_id",
                                            "customer_email", "plan", "status", "test")})
                        except Exception:
                            pass
            return self._json(200, {"generated_at": now_iso(),
                                    "secret_configured": bool(SECRET),
                                    "subscriptions": subs,
                                    "entitlements": ent,
                                    "recent_events": recent})
        return self._json(404, {"error": "not-found"})

    def log_message(self, fmt, *args):
        print(f"[{now_iso()}] {self.address_string()} {fmt % args}", flush=True)


if __name__ == "__main__":
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    load_seen_ids()
    print(f"[{now_iso()}] dd-dodo-webhook listening on {LISTEN_HOST}:{LISTEN_PORT} "
          f"(secret_configured={bool(SECRET)})", flush=True)
    ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), Handler).serve_forever()
