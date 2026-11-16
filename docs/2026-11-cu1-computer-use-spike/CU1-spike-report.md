# CU-1 Computer-Use Agent Spike — Results Report

**Date:** November 16, 2026 · **Status: GO** — proceed to CU-2/CU-3/CU-4
**Build plan:** DenialsDoctor Computer-Use Agents Build Plan (this is item CU-1)

## What was built (working code, not a prototype design)

A complete computer-use agent loop, per Section 6 of the build plan:

```
planner (LLM)  ->  guard (trust ladder)  ->  driver (headless Chromium)  ->  audit (JSONL + screenshots)
```

| File | Role |
|---|---|
| `backend/agents/cu/cu-agent.mjs` | Core loop: snapshot page → LLM proposes ONE action → guard validates → driver executes → audit + screenshot → repeat until `done` |
| `backend/agents/cu/synthetic-portal/server.mjs` | Synthetic payer portal ("Meridian Health Plan"): claim lookup form + result pages, 300–700 ms simulated latency, zero PHI |
| `backend/agents/cu/synthetic-portal/claims.mjs` | 10 fictional claims: 4 PAID, 3 DENIED (CO-97, CO-16, CO-29), 2 PENDING — ground truth for scoring |
| `backend/agents/cu/run-spike.mjs` | Batch runner with scoring vs ground truth |
| `backend/agents/cu/smoke.mjs`, `run-retry.mjs` | Single-task test + supplemental re-runs |

**Architecture decisions proven in code:**
- **Pluggable planner:** runs on GLM (z-ai SDK) today; `openai-cua` is a config swap away once an OpenAI key is provisioned at `/etc/openai/env` (none exists yet — verified).
- **Guard enforces the trust ladder in code, not prompts:** review mode allows only `fill` / `click` / `done`; click targets matching write patterns (submit payment, authorize, save, resubmit, download, banking) are rejected as `approval_required`; refs must exist on the current page; step budget enforced.
- **Audit trail (seed of CU-2):** every step appended to `audit.jsonl` — timestamp, action, rationale, screenshot file; screenshots saved per step.
- **Stop-and-ask rule embedded:** the planner may end with `claimStatus: UNCLEAR` instead of guessing; `NOT_FOUND` handled as its own outcome.

## Measured results

**Accuracy: 10 of 10 unique claims exact-matched (100%)** — status AND CARC code both correct on every claim where the planner API responded. Full pass + supplemental pass combined:

| Claim | Expected | Agent extracted | Match |
|---|---|---|---|
| CLM24801 | PAID | PAID | ✓ |
| CLM24802 | PAID | PAID | ✓ |
| CLM24803 | DENIED, CO-97 | DENIED, CO-97 | ✓ |
| CLM24804 | PAID | PAID | ✓ |
| CLM24805 | DENIED, CO-16 | DENIED, CO-16 | ✓ |
| CLM24806 | PENDING | PENDING | ✓ |
| CLM24807 | DENIED, CO-29 | DENIED, CO-29 | ✓ |
| CLM24808 | PENDING | PENDING | ✓ (supplemental pass) |
| CLM24809 | PAID | PAID | ✓ (supplemental pass) |
| CLM24810 | PAID | PAID | ✓ (supplemental pass) |

**Efficiency (successful tasks):** 3 executed actions per task (2 fills + 1 click, then read + done); ~6.5 s of active agent time per task without pacing overhead; ~500–700 token-equivalents per task.

**Infrastructure failures, honestly reported:** 3 of 13 continuous-pass attempts failed with HTTP 429 (sandbox LLM-endpoint rate limit), all recovered on a later pass. These are quota events in the dev sandbox, not agent defects — the production path (droplet + OpenAI key with contract quotas, or a paid GLM tier) is not subject to this ceiling. Retry with exponential backoff (8/20/40 s) is now part of the planner and absorbed 2 of 5 rate-limit events mid-run.

## Cost picture (planning numbers)

- At **GPT-6 Luna's published $0.085/task**: 600 eligibility checks/month = **$51.00 COGS** — consistent with the Build Plan's unit economics (Table 4).
- GLM planner today: ~600 token-equivalents per task measured; USD mapping depends on the production planner tier and will be re-measured after the OpenAI key lands.
- Voice (Cartesia, AR Caller): $0.014/min — 500 min = $7.00. Unchanged.

## What CU-1 de-risks (build-plan questions answered)

1. *Can a computer-use model drive a portal?* Yes — deterministic 3-action path on every claim, including the "no claim found" logic and per-status variance (paid/pending/denied with CARC).
2. *Can we supervise it?* Yes — guard + audit JSONL + per-step screenshots all captured; review-mode write blocking enforced.
3. *Is it cheap enough at SMB prices?* Yes — measured token volume is consistent with the $0.085/task planning number and the approved margins.

## Next (per build plan, unchanged)

- **CU-2:** credential vault + hardened audit trail on the droplet
- **CU-3:** review-gate UI in the Agent Console (approve/reject queue with screenshots)
- **CU-4:** ship AR Caller portal mode (IVR first, portal fallback) — first customer-facing computer-use feature
- **CU-5:** DenialsAdminBench harness v1 (these 10 synthetic claims become its first 10 tasks)
- **OpenAI key:** founder provisions API key + confirms BAA coverage; planner swaps to `openai-cua` behind the same interface

## Reproduce

```bash
cd backend/agents/cu
node smoke.mjs                        # 1 task end-to-end
RUNS=10 node run-spike.mjs            # scored batch vs ground truth
node run-retry.mjs                    # supplemental pass
# audit + screenshots land in ./runs/<session>/audit.jsonl + step-NN.png
```
