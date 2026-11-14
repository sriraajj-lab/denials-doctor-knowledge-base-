"""DenialsDoctor — checkout-to-account provisioning bridge (v3.8).

Closes the fulfillment gap in the purchase journey: a successful Dodo
subscription event must produce a working login without human intervention.

Endpoints:
  POST /internal/provision            — called by the webhook receiver on a
                                        granted subscription event (shared
                                        secret, localhost traffic only).
  GET  /auth/set-password/verify      — token validity check for the
                                        set-password page.
  POST /auth/set-password             — buyer sets their own password.

Security contract:
- /internal/provision requires header `X-Internal-Secret` matching the
  INTERNAL_PROVISION_SECRET env var (constant-time compare). The receiver
  runs on the same host and calls it over loopback only.
- Password tokens are 32-byte urlsafe secrets; only their sha256 hash is
  stored, they expire in 24h, are single-use, and issuing a new one
  invalidates the buyer's previous unused tokens.
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import time
from typing import Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field

from .audit import log as audit_log
from .auth import hash_password
from .db import get_conn, _now_iso, _uuid
from . import service

router = APIRouter()

TOKEN_TTL_SECONDS = 24 * 3600
PASSWORD_MIN_LEN = 10
PLAN_PATTERN = r"^(starter|pro|enterprise)$"


def _internal_secret() -> str:
    return os.environ.get("INTERNAL_PROVISION_SECRET", "").strip()


def _ensure_tables() -> None:
    with get_conn() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS password_tokens (
                   token_hash TEXT PRIMARY KEY,
                   user_id    TEXT NOT NULL,
                   email      TEXT NOT NULL,
                   expires_at TEXT NOT NULL,
                   used       INTEGER NOT NULL DEFAULT 0,
                   created_at TEXT NOT NULL
               )"""
        )


_ensure_tables()


def _sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class ProvisionRequest(BaseModel):
    email: EmailStr
    plan: str = Field(..., pattern=PLAN_PATTERN)
    company_name: Optional[str] = None
    product_id: Optional[str] = None
    subscription_id: Optional[str] = None
    customer_id: Optional[str] = None
    source: str = "dodo-webhook"


class ProvisionResponse(BaseModel):
    status: str
    client_id: str
    user_id: str
    email: str
    plan: str
    created_client: bool
    created_user: bool
    password_token: Optional[str] = None
    set_password_url: Optional[str] = None
    note: str = ""


class SetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=16)
    password: str = Field(..., min_length=PASSWORD_MIN_LEN)


def _client_for_billing_email(email: str) -> Optional[dict]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, settings, plan, name FROM clients WHERE deleted_at IS NULL"
        ).fetchall()
    for row in rows:
        try:
            settings = json.loads(row["settings"] or "{}")
        except Exception:
            continue
        if (settings.get("billing_email") or "").lower() == email.lower():
            return {"id": row["id"], "plan": row["plan"], "name": row["name"]}
    return None


def _issue_password_token(user_id: str, email: str) -> tuple[str, str]:
    """Create a single-use set-password token. Returns (raw_token, expires_at)."""
    raw = secrets.token_urlsafe(32)
    now = time.time()
    expires_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now + TOKEN_TTL_SECONDS))
    with get_conn() as conn:
        # invalidate previous unused tokens for this user
        conn.execute("DELETE FROM password_tokens WHERE user_id = ? AND used = 0", (user_id,))
        conn.execute(
            """INSERT INTO password_tokens (token_hash, user_id, email, expires_at, used, created_at)
               VALUES (?, ?, ?, ?, 0, ?)""",
            (_sha256_hex(raw), user_id, email, expires_at, _now_iso()),
        )
    return raw, expires_at


@router.post("/internal/provision", response_model=ProvisionResponse)
def provision(body: ProvisionRequest, request: Request):
    supplied = request.headers.get("X-Internal-Secret", "")
    expected = _internal_secret()
    if not expected or not secrets.compare_digest(supplied, expected):
        raise HTTPException(status_code=403, detail="forbidden")

    email = body.email.lower()
    ip = getattr(request.state, "ip", "") or (request.client.host if request.client else "")

    user = service.get_user_by_email(email)
    created_client = False
    created_user = False
    note = ""

    if user is None:
        client = _client_for_billing_email(email)
        if client is None:
            name = (body.company_name or email.split("@")[0])[:80]
            client = service.create_client(
                name=name,
                plan=body.plan,
                settings_json={
                    "billing_email": email,
                    "product_id": body.product_id,
                    "subscription_id": body.subscription_id,
                    "customer_id": body.customer_id,
                    "source": body.source,
                },
            )
            created_client = True
        client_id = client["id"]
        # placeholder password: never disclosed; the buyer sets their own via
        # the single-use token. Login is impossible until set-password completes.
        placeholder = secrets.token_urlsafe(24)
        user = service.create_user(client_id=client_id, email=email,
                                   password=placeholder, role="client_admin")
        created_user = True
    else:
        client_id = user["client_id"]

    # keep plan + billing metadata current on every granted event
    with get_conn() as conn:
        conn.execute("SELECT id FROM clients WHERE id = ?", (client_id,)).fetchone()
    client_now = service.get_client(client_id)
    settings = {}
    if client_now and client_now.get("settings"):
        try:
            settings = json.loads(client_now["settings"])
        except Exception:
            settings = {}
    settings.update({
        "billing_email": email,
        "subscription_id": body.subscription_id or settings.get("subscription_id"),
        "product_id": body.product_id or settings.get("product_id"),
        "customer_id": body.customer_id or settings.get("customer_id"),
    })
    service.update_client(client_id, plan=body.plan, settings_json=settings)

    issue_token = created_user or not user.get("last_login_at")
    raw_token = None
    if issue_token:
        raw_token, _ = _issue_password_token(user["id"], email)
        note = "new-user-welcome" if created_user else "activation-resend"
    else:
        note = "existing-active-user-no-token"

    base = os.environ.get("PUBLIC_APP_ORIGIN", "https://denialsdoctor.com").rstrip("/")
    set_url = f"{base}/welcome/set-password?token={raw_token}" if raw_token else None

    audit_log(
        client_id=client_id, user_id=user["id"], user_email=email,
        action="internal.provision",
        target=f"client:{client_id}",
        ip=ip or None,
        details={"plan": body.plan, "created_client": created_client,
                 "created_user": created_user, "source": body.source,
                 "subscription_id": body.subscription_id},
    )
    return ProvisionResponse(
        status="ok", client_id=client_id, user_id=user["id"], email=email,
        plan=body.plan, created_client=created_client, created_user=created_user,
        password_token=raw_token, set_password_url=set_url, note=note,
    )


@router.get("/auth/set-password/verify")
def verify_set_password(token: str):
    row = None
    with get_conn() as conn:
        row = conn.execute(
            """SELECT email, expires_at, used FROM password_tokens WHERE token_hash = ?""",
            (_sha256_hex(token),),
        ).fetchone()
    if row is None or row["used"]:
        return {"valid": False}
    if row["expires_at"] <= _now_iso():
        return {"valid": False}
    return {"valid": True, "email": row["email"]}


@router.post("/auth/set-password")
def set_password(body: SetPasswordRequest, request: Request):
    with get_conn() as conn:
        row = conn.execute(
            """SELECT token_hash, user_id, email, expires_at, used
                 FROM password_tokens WHERE token_hash = ?""",
            (_sha256_hex(body.token),),
        ).fetchone()
    if row is None or row["used"] or row["expires_at"] <= _now_iso():
        raise HTTPException(status_code=400, detail="This set-password link is invalid or has expired. Contact support@denialsdoctor.com for a new one.")

    user = service.get_user_by_email(row["email"])
    if user is None or user["id"] != row["user_id"]:
        raise HTTPException(status_code=400, detail="Account not found for this link.")

    with get_conn() as conn:
        conn.execute(
            "UPDATE users SET password_hash = ?, updated_at = ? WHERE id = ?",
            (hash_password(body.password), _now_iso(), user["id"]),
        )
        conn.execute("UPDATE password_tokens SET used = 1 WHERE token_hash = ?", (row["token_hash"],))

    ip = getattr(request.state, "ip", None)
    audit_log(
        client_id=user["client_id"], user_id=user["id"], user_email=user["email"],
        action="user.password_set", ip=ip,
    )
    return {"status": "ok", "email": user["email"]}
