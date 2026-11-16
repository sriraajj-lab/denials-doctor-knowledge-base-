# CU Agent — Provider Guide (answer: NOT OpenAI-only)

**Date:** November 16, 2026

## Direct answer

The computer-use agent is **provider-agnostic**. It does NOT need an OpenAI key. The planner is a swappable module that speaks to any chat-completions API:

| Planner | Status | How it connects |
|---|---|---|
| **`compat` — ANY OpenAI-compatible endpoint** | ✅ **LIVE-PROVEN** (OpenRouter free tier) | 3 env vars: `PLANNER_BASE_URL`, `PLANNER_API_KEY`, `PLANNER_MODEL` |
| `glm` — z-ai SDK | ✅ live-proven (10/10 spike) | built into the dev sandbox |
| `openai-cua` — OpenAI computer-use model | pending founder key | `/etc/openai/env`; adds screenshot-based coordinate actions |

Because the planner consumes **structured accessibility snapshots** (not raw screenshots), any capable text/vision chat model can drive the loop — Groq, Google Gemini, Cerebras, Together, DeepSeek, Mistral, or a self-hosted vLLM/Ollama endpoint all work through the same `compat` client. OpenAI's CUA remains valuable later specifically for screenshot/coordinate precision on messy portals, but it is not a requirement.

## What is connected RIGHT NOW (free, zero sign-up needed)

An **OpenRouter API key already provisioned** (stored at `scripts/dd-fulfillment/openrouter.env`, mode 0600, also on the droplet at `/etc/denials-doctor/env`) is now wired in and **live-tested**:

- Smoke: CLM24803 → DENIED + CO-97, exact, 3 steps
- Batch: **5/5 exact match (100% success rate)**, 3.0 actions/task, 22.8 s/task avg, ~933 tokens/task (real API usage numbers)
- Model used: `nvidia/nemotron-3-ultra-550b-a55b:free` (550B MoE, 1M context — strongest free variant on the key at time of test; 17 free variants were available)
- Cost so far: **$0.00** (free-tier requests; key shows usage 0 credits)

## Free-tier landscape (verified Nov 2026, cite at sign-up time)

| Provider | Free tier | Practical for CU agent? | Sign-up |
|---|---|---|---|
| **OpenRouter** | 20 req/min, **50 req/day** on `:free` models (<$10 all-time credits); **1,000/day** once ≥$10 credits purchased (one-time, unlocks permanently) | ✅ connected today; 50/day ≈ 10 agent tasks/day; 1,000/day ≈ 200 tasks/day | [openrouter.ai](https://openrouter.ai) — already done |
| **Groq** | ~30 req/min; 1,000–14,400 req/day depending on model | ✅ good redundancy option; ultra-low latency | [console.groq.com](https://console.groq.com/docs/rate-limits) |
| **Google AI Studio (Gemini)** | free tier with per-day/per-minute limits on Flash models | ✅ vision-capable (future screenshot mode) | [aistudio.google.com](https://aistudio.google.com) |
| Cerebras / Mistral / Together | free or trial tiers, per-model caps | optional redundancy | each provider's own console |
| Self-hosted (vLLM/Ollama) | unlimited, hardware-bounded | full control, no PHI leaves the droplet | n/a |

Sources: [OpenRouter limits doc](https://openrouter.ai/docs/api_reference/limits) (20/min, 50/day < $10 credits; 1,000/day ≥ $10; extra keys/accounts do not raise caps; honor `Retry-After`), [Groq rate-limits doc](https://console.groq.com/docs/rate-limits).

## Recommendation (unchanged production math)

1. **Dev/validation now:** OpenRouter free tier — connected, proven, $0.
2. **Production droplet:** buy $10 of OpenRouter credits once (unlocks 1,000 free-model requests/day ≈ 200 claim checks/day at no marginal model cost), **or** use paid variants for the volumes in the build plan; the $0.085/task GPT-6 Luna number stays the production planning figure.
3. **When the founder provisions the OpenAI key:** flip `openai-cua` on for screenshot-based CUA; the guard/audit layer is provider-independent, so supervision stays identical.

## Connect / switch providers in 5 minutes

```bash
# 1. put the key in an env file (0600), e.g. scripts/dd-fulfillment/openrouter.env:
#    OPENROUTER_API_KEY=sk-or-v1-...
# 2. run the agent with three env vars:
set -a; source scripts/dd-fulfillment/openrouter.env; set +a
export PLANNER_BASE_URL="https://openrouter.ai/api/v1"   # or Groq/Gemini/Cerebras/self-hosted
export PLANNER_MODEL="nvidia/nemotron-3-ultra-550b-a55b:free"
RUNS=10 node run-spike.mjs     # or smoke.mjs for one task
```

Switching providers = changing those three variables. No code changes. The guard (review-mode write blocking), audit JSONL, and screenshots work identically on every provider.

## Verification trail

- OpenRouter key status: `is_free_tier: true`, usage 0, free-model daily limit 50 (checked live via `/api/v1/key`)
- Smoke + 5-task batch on `:free` Nemotron: 6/6 exact match, no 429s (4s pacing stays under the 20/min cap)
- GLM planner (previous run): 10/10 exact match — both planners produce identical task outcomes through the same guard
