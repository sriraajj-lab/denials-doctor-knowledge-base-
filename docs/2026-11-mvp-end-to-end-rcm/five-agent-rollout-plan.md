# Five-Agent Rollout Plan (and the EHR agent)

**Date:** November 17, 2026 · Owner: Rajesh (DenialsDoctor) · Scope: product + go-to-market sequencing for the MVP shipped today

## What shipped (the base)

| Component | State | Proof |
|---|---|---|
| Agent Console (accounts, entitlements, audit) | live at denialsdoctor.com/console | 16/16 E2E checks incl. entitlement gates |
| Eligibility Agent (270/271) | live | sandbox payer verified; live-payer webhook hook ready |
| Coding Agent (rules + optional LLM) | live | fixture findings with confidence scores |
| Payment Posting Agent (.835) | live | CARC grouping + underpayment scan |
| Biller Agent (837P 5010) | live | clean-claim file generated, holds with reasons |
| AR Caller Agent (worklist + scripts) | live | per-CARC scripts, SLA owners, recheck tasks |
| EHR Computer-Use Agent (SoM + vision LLM, Playwright) | live, review-mode | DENIED+CO-97 exact, screenshot audit, guard blocks writes |
| Billing (Dodo LIVE) | live | 5 per-agent SKUs + bundle; auto-provisioning to Console + welcome email |

## Rollout sequence (recommended)

**Week 1-2 — Design partners (3-5 practices).** Sell one agent per practice (start with Payment Posting — fastest time-to-value on their real .835s). Founder does onboarding calls personally. Success metric: first real remittance processed within 24h of signup, underpayment/denial numbers verified by the practice.

**Week 3-4 — Real payer connectivity for Eligibility.** Contract with a clearinghouse (Availity, Change, Stedi) or office-ally-style endpoint; wire `ELIGIBILITY_WEBHOOK_URL`; add per-payer 271 quirks to the parser. Metric: ≥90% real-271 parse rate across top-10 payers.

**Week 5-6 — EHR agent portal adapters.** Move from URL-targeted review-mode to per-payer portal presets (Availity first — highest claim-status volume), then enable the hybrid loop from the build plan: accessibility refs primary, SoM visual fallback. Still read-only. Metric: 50 real claim re-verifications/day across pilots with zero guard blocks.

**Week 7-8 — Write actions with the review gate.** Ship the CU-3 approve/reject queue: every write-class portal action (resubmission, claim inquiry) requires human approval in the Console before execution; screenshots before/after attached automatically. This converts the agent from "verification" to "action with supervision" — the AR Caller's scripts start closing dollars.

**Week 9-12 — AR Caller voice layer + scale.** Add the phone follow-up lane (existing DD Live Agents infrastructure) for high-value denials; bundle reporting (recovered-$ dashboard per practice); raise GA pricing for new accounts; move founding customers to annual plans at a discount.

## Pricing ladder (live on Dodo)

| SKU | Price | Purpose |
|---|---|---|
| Eligibility Agent | $49/mo | land |
| Coding Agent / Posting Agent | $99/mo | expand |
| Biller Agent | $149/mo | expand |
| AR Caller Agent | $199/mo | expand |
| Full Suite + EHR Agent | $99/mo founding → $349/mo GA | bundle anchor |

## Risks and mitigations

- **HIPAA posture:** portal actions are read-only today; no PHI in AI prompts by default; audit JSONL + screenshots are the compliance story. Before write-actions GA: sign BAAs, encrypt audit artifacts at rest, retention policy.
- **Payer portal fragility:** SoM is proven on structured portals; keep per-portal adapters versioned, cap agent runs per portal, and keep the review gate mandatory for writes.
- **Support load:** self-serve sample datasets + per-row error messages are built in; design-partner phase calibrates onboarding docs before volume marketing.
