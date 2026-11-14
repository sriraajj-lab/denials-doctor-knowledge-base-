# DenialsDoctor — AI Revenue Cycle Agent

DenialsDoctor is a healthcare revenue-cycle SaaS that helps medical and dental
practices recover denied insurance claims. The product analyzes denied claims
(CARC codes), drafts appeal letters, tracks outcomes, and is expanding into
five AI agents (AR Caller, Eligibility & Verification, Medical Coder, Payment
Posting, Medical Biller) that ship as console modules between December 2026
and February 2027.

This repository contains the customer-facing fulfillment layer that was built
and verified on **November 13, 2026**: the checkout-to-account provisioning
bridge, the payment webhook receiver, the post-purchase web pages, and the
operations scripts that deploy and verify them.

## Live surfaces

| Surface | URL | Purpose |
|---|---|---|
| Marketing site | https://denialsdoctor.com | Homepage, agents storefront, pricing |
| Pricing / checkout | https://denialsdoctor.com/start | Three plans, each linking to Dodo's hosted checkout |
| Post-purchase confirmation | https://denialsdoctor.com/welcome | "Trial started — check your inbox" page |
| Set-password page | https://denialsdoctor.com/welcome/set-password | Single-use token → buyer sets their own password |
| Sign-in | https://denialsdoctor.com/login | Buyer login (email + password) |
| Denial Desk (console v0) | https://denialsdoctor.com/app | Add denial → analyze → track outcomes |
| Free tools (no account) | https://denialsdoctor.com/appeal-letter-generator · /denial-code | Lead magnets feeding the funnel |
| Webhook receiver | https://denialsdoctor.com/api/webhooks/dodo | Dodo Payments delivery target |

## Architecture (single droplet)

```
Cloudflare DNS → Caddy (reverse proxy)
                 ├─ Next.js static marketing site   (port 3100, /var/www/denialsdoctor)
                 ├─ FastAPI backend v3.7            (port 8000, /opt/denials-doctor-v37)
                 │    ├─ /auth/*            login, sessions (Argon2, 12h tokens)
                 │    ├─ /denials/*         encrypted denial records (AES-GCM per client)
                 │    ├─ /denials/analyze   tiered LLM failover chain (tier 6 = OpenRouter)
                 │    ├─ /internal/provision  ← shared-secret, loopback-only
                 │    └─ /auth/set-password   single-use token flow
                 └─ dd-dodo-webhook receiver        (port 8787, Python stdlib HTTP server)
                      ├─ signature verification (Standard Webhooks scheme)
                      ├─ entitlements state     (/var/lib/dd-dodo-webhook/*.json)
                      ├─ → calls /internal/provision over loopback
                      └─ → sends welcome + admin-notification email (Zoho Mail API)
```

Dodo products: Starter $99 / Professional $299 / Enterprise $799 per month,
15-day free trial, card required, $0.00 due today. Aria Managed tiers
($497 / $997 / $1,997) are done-for-you services — they send an
onboarding-contact email instead of provisioning a console account.

## The fulfillment flow (automated, verified end-to-end)

1. Buyer completes Dodo checkout → Dodo fires `subscription.active`.
2. Webhook receiver verifies the signature, maps product → plan, records the
   entitlement.
3. Receiver calls the backend's internal provisioning endpoint (shared secret,
   loopback traffic only; the API gateway 404s any external request for
   `/internal/*`).
4. Backend creates the client (workspace) with the bought plan and an admin
   user for the buyer's email, then issues a **single-use set-password token**
   (32-byte, stored hashed, 24-hour expiry; issuing a new one invalidates the
   old). Re-provisioning on renewal is idempotent — no duplicate accounts, no
   re-sent password emails to active users.
5. Receiver emails the buyer a welcome message with the set-password link and
   copies the owner on a fulfillment notification (real-time monitoring).
6. Buyer sets a password, signs in, and runs their first denial analysis on
   the Denial Desk.

Every step is written to a hash-chained audit log. Test-mode webhook events
are processed but skip provisioning/email unless `PROVISION_TEST_EVENTS=1`.

## Repository map

```
docs/       Customer journey, QA findings, master rollout plan (docx + pdf)
backend/    provisioning.py — FastAPI router: /internal/provision,
            /auth/set-password[/verify], password_tokens table
webhook/    receiver.py — Dodo webhook receiver + fulfillment bridge;
            selftest.py — signed-event self-test harness
web/        welcome.html, welcome/set-password.html, login.html, console.html
scripts/    deploy_fulfillment.py  (rollback-safe deploy of the whole bridge)
            deploy_tier6.py       (adds OpenRouter as LLM tier 6)
            e2e_test.py           (provision→verify→set-password→login→plan)
            webhook_chain_test.py (signed event → provision → email, on droplet)
            smtp_probe.py, qwen_probe.py, or_free_models.py (provider probes)
```

## Configuration (all secrets via environment, never in code)

Backend (`/etc/denials-doctor/env`): `INTERNAL_PROVISION_SECRET`,
`PUBLIC_APP_ORIGIN`, `OPENROUTER_API_KEY`, plus the pre-existing auth/LLM
settings.

Webhook receiver (`/etc/dd-dodo-webhook/env`): `DODO_WEBHOOK_KEY`,
`ADMIN_TOKEN`, `INTERNAL_PROVISION_SECRET`, `BACKEND_INTERNAL_URL`,
`ADMIN_NOTIFY_EMAIL`, `MAIL_FROM_ADDRESS`, `ZOHO_CLIENT_ID`,
`ZOHO_CLIENT_SECRET`, `ZOHO_REFRESH_TOKEN`, `ZOHO_ACCOUNT_ID`,
`ZOHO_TOKEN_URL`, `PROVISION_TEST_EVENTS`.

**Secrets are deliberately excluded from this repository.** The `.gitignore`
blocks key files, env files, credentials sheets, and session dumps; the
deployment scripts read them from protected files at deploy time.

## Verification summary (November 13, 2026)

- API chain test (provision → verify token → set password → single-use
  rejection → login → plan reflected): **all checks passed**
- Signed webhook through the public endpoint → `provision=ok mail=ok` in the
  receiver log; admin notification delivered to the founder's inbox
- Real-browser click-through: set-password → sign-in → Denial Desk → live
  CO-97 analysis (18.4 s) saved to the workspace
- Edge states (invalid/expired token, logged-out console, public access to
  internal endpoints) return clear copy or 404, never dead ends

See `docs/DenialsDoctor-Customer-Journey-Subscription-to-Implementation.pdf`
for the full journey narrative and
`docs/DenialsDoctor-Purchase-Journey-QA-Findings.pdf` for the audit that
motivated these fixes.

## Known operational items

- The analysis engine's earlier LLM tiers are decommissioned/exhausted; tier 6
  (OpenRouter, free model) is the working stopgap with a daily request cap —
  a small credit top-up lifts it ~20×, and restoring a primary paid model is
  the durable fix.
- Per-agent Dodo products, the Agent Console modules, and the AR caller's
  voice loop are on the build schedule in the Master Rollout Plan.
