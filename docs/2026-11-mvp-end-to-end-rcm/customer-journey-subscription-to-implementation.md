# Customer Journey: Subscription → Implementation

**Date:** November 17, 2026 · Applies to denialsdoctor.com MVP (five RCM agents + EHR computer-use agent)

## The journey, end to end

**1. Discover (public marketing).** The founder points prospects at [denialsdoctor.com/rcm-suite](https://denialsdoctor.com/rcm-suite) — the end-to-end RCM pitch with per-agent pricing and the founding-offer bundle. Every card carries a live Dodo checkout button (15-day free trial, card required at signup, cancel anytime; nothing is charged during the trial).

**2. Subscribe (Dodo LIVE checkout).** The buyer pays through Dodo. Five per-agent SKUs are live: Eligibility $49/mo, Coding $99/mo, Payment Posting $99/mo, Biller $149/mo, AR Caller $199/mo — plus the existing Starter bundle at $99/mo founding (GA anchor $349) which unlocks all six agents.

**3. Provision (automatic, zero human touch).** A granted subscription event hits the Dodo webhook receiver, which now (a) runs the existing fulfillment bridge for the main platform account, and (b) provisions the buyer's **Agent Console** account at denialsdoctor.com/console, appending the purchased product to their entitlement map. The buyer receives a "Your Agent Console is ready" email with their login (temporary password if new, or "log in with existing credentials"). This path was verified live; failures in the email/provision step are logged and never block checkout.

**4. First run (self-serve, minutes).** At /console the buyer sees one card per agent, locked or active according to what they bought. Entitlement enforcement is server-side: an unsubscribed agent returns a 403 with an upgrade link. Each agent takes a paste-CSV (or .835) input, offers a one-click sample dataset, and returns: a summary report, per-row results, and downloadable artifacts (270/271 EDI, 837P claim file, posting ledger, coding findings, AR worklists).

**5. Delegate to the EHR agent.** The EHR Computer-Use Agent card runs the SoM (Set-of-Mark) browser agent against a payer/EHR portal: it fills claim + DOB, searches, reads the result page with a vision LLM, and returns claim status / CARC / amounts with a full screenshot. Review-mode is enforced: it is read-only; forbidden actions (payments, saves, submissions) are blocked by the guard and logged.

**6. Audit.** Every login, agent run, per-agent step, and EHR action lands in the per-customer audit trail (JSONL), visible in the Console's Audit section. Operational state lives on the droplet (`/var/lib/dd-console/`).

## What the founder can market today

- End-to-end RCM claim: eligibility → coding → clean claims → posting → AR follow-up → portal re-verification, all agent-driven with audit trails.
- Per-agent unbundled pricing for practices that want one piece first (land-and-expand).
- The founding offer ($99/mo all-in) as the anchor with a $349 GA price.

## Known limits (state plainly in sales conversations)

- Payer connectivity for eligibility is a deterministic sandbox payer; a real clearinghouse/payer webhook hooks in via one env var (`ELIGIBILITY_WEBHOOK_URL` + "live payer" option).
- The EHR agent is read-only in this release and targets one portal at a time by URL; per-payer portal adapters come in the rollout plan.
- Coding Agent's LLM second review uses a free-tier model by default (deterministic rules always run); no PHI leaves the droplet unless a customer enables LLM review.
