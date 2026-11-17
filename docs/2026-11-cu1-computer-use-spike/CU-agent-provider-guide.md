# CU Agent — Provider Guide (answer: NOT OpenAI-only) + CUA screenshot-mode alternates

**Date:** November 17, 2026 (v2 — corrected & extended)

## Correction of record (transparency first)

The v1 of this guide claimed a "5/5 batch on OpenRouter free". **That was wrong**: the batch runners defaulted to `planner: "glm"` when the `PLANNER` env var was unset, so those 5/5 results were produced by the GLM planner (z-ai SDK), not OpenRouter. The bug was caught when the visual-mode demo read `PLANNER_API_KEY` strictly and refused to start. Fixes applied and **genuinely re-verified on OpenRouter free**:

- compat **text planner** (Nemotron 550B `:free`): CLM24803 → DENIED + CO-97 **exact**, 3 steps, 41.7 s, ~3,350 token-equiv/task
- compat **vision mode** (Nemotron VL `:free`): full visual claim lookup → **exact match** (see below), ~3,461 real tokens
- Ergonomics guardrail added: the compat client now accepts `OPENROUTER_API_KEY` directly, so sourcing the env file is sufficient; runners require explicit `PLANNER=compat` to leave the default.

GLM numbers (10/10 spike, 5/5 batch, ~933 tok/task) stand as stated — they were real, just attributed to the wrong planner.

## Direct answer

The computer-use agent is **provider-agnostic**. It does NOT need an OpenAI key. The planner is a swappable module that speaks to any chat-completions API:

| Planner | Status | How it connects |
|---|---|---|
| **`compat` — ANY OpenAI-compatible endpoint** | ✅ **live-proven on OpenRouter free** (text + vision) | env vars: `PLANNER_BASE_URL`, `PLANNER_API_KEY` (or `OPENROUTER_API_KEY`), `PLANNER_MODEL` |
| `glm` — z-ai SDK | ✅ live-proven (10/10 spike) | built into the dev sandbox |
| `openai-cua` — OpenAI computer-use model | pending founder key | `/etc/openai/env`; adds raw screenshot+coordinate actions |

# The alternate for CUA screenshot mode: Set-of-Mark (SoM) visual mode

**Built and live-proven today, on a free vision model, $0.00 spent.** OpenAI's CUA takes a raw screenshot and returns pixel coordinates. The provider-agnostic alternative replaces coordinates with **numbered marks**:

1. **Annotate:** inject red numbered badges over every visible interactive element in the live DOM (no image processing needed) — `som.mjs`
2. **Perceive:** screenshot the annotated page → any vision chat model sees "badge 1 = claim input, badge 2 = DOB input, badge 3 = Search Claims button"
3. **Act:** the model answers with a mark **number** (robust, no pixel math), driver clicks/fills the real element via that mark
4. **Read:** screenshot the result page → vision model extracts claim status fields as JSON

**Live result** (`som-demo.mjs`, model `nvidia/nemotron-3.5-super-vl:free` via OpenRouter):
- Vision correctly identified all 3 marks: `{"claimMark":1,"dobMark":2,"searchMark":3}`
- Full task completed: form filled, search clicked (real URL navigation), result page read
- Extraction: `{"claimStatus":"DENIED","carcCode":"CO-97","paidAmount":"$0.00","statusDate":"2026-11-05"}` — **exact match** vs ground truth
- Cost: ~3,461 tokens, **$0.00**

So the three interaction modes the agent now has:

| Mode | Input to model | Output | Status | Best for |
|---|---|---|---|---|
| **A. Accessibility refs** (primary) | structured DOM text with `@e` refs | JSON action w/ ref | ✅ 10/10 + 5/5 + 1/1 proven | clean portals, forms, tables — cheaper (~900 tok/task) |
| **B. SoM visual** (fallback) | annotated screenshot + mark list | mark number + JSON extract | ✅ proven today on free VLM | JS-heavy portals, canvas widgets, missing ARIA labels, CAPTCHA-adjacent UI |
| **C. OpenAI CUA** | raw screenshot | pixel coordinates | optional later | marginal gain over B; only if a portal defeats both A and B |

**Production architecture: hybrid A→B.** Try accessibility refs first (cheap, deterministic); if the snapshot comes back empty or the guard rejects repeated actions, switch to SoM visual mode automatically. Screenshots are captured either way for the CU-3 review gate — human approvers see exactly what the agent saw.

## What is connected RIGHT NOW (free, zero sign-up needed)

An **OpenRouter API key already provisioned** (stored at `scripts/dd-fulfillment/openrouter.env`, mode 0600, also on the droplet at `/etc/denials-doctor/env`) is wired in, with both planner paths **genuinely live-verified**:

- Text planner: smoke task exact match (see correction note above)
- Visual mode: full claim lookup exact match, $0.00
- Models used: `nvidia/nemotron-3-ultra-550b-a55b:free` (text), `nvidia/nemotron-3.5-super-vl:free` (vision) — 17 free variants were available on the key
- Key status checked live: `is_free_tier: true`, usage 0 credits, free-model daily limit 50

## Free-tier landscape (verified Nov 2026, cite at sign-up time)

| Provider | Free tier | Practical for CU agent? | Sign-up |
|---|---|---|---|
| **OpenRouter** | 20 req/min, **50 req/day** on `:free` models (<$10 all-time credits); **1,000/day** once ≥$10 credits purchased (one-time, unlocks permanently) | ✅ connected today; 50/day ≈ 10 agent tasks/day; 1,000/day ≈ 200 tasks/day | [openrouter.ai](https://openrouter.ai) — already done |
| **Groq** | ~30 req/min; 1,000–14,400 req/day depending on model | ✅ good redundancy option; ultra-low latency | [console.groq.com](https://console.groq.com/docs/rate-limits) |
| **Google AI Studio (Gemini)** | free tier with per-day/per-minute limits on Flash models; vision-capable | ✅ strong SoM vision candidate | [aistudio.google.com](https://aistudio.google.com) |
| Cerebras / Mistral / Together | free or trial tiers, per-model caps | optional redundancy | each provider's own console |
| Self-hosted (vLLM/Ollama) | unlimited, hardware-bounded | full control, no PHI leaves the droplet | n/a |

Sources: [OpenRouter limits doc](https://openrouter.ai/docs/api_reference/limits) (20/min, 50/day < $10 credits; 1,000/day ≥ $10; extra keys/accounts do not raise caps; honor `Retry-After`), [Groq rate-limits doc](https://console.groq.com/docs/rate-limits).

## Recommendation (production math unchanged)

1. **Dev/validation now:** OpenRouter free tier — connected, both modes proven, $0.
2. **Production droplet:** buy $10 of OpenRouter credits once (unlocks 1,000 free-model requests/day ≈ 200 claim checks/day), or use paid variants for build-plan volumes; the $0.085/task GPT-6 Luna number stays the production planning figure.
3. **OpenAI CUA:** optional, not blocking — SoM visual mode already covers the screenshot use case on free/paid models of any vendor.

## Connect / switch providers in 5 minutes

```bash
# 1. key file (0600) — OPENROUTER_API_KEY is accepted directly:
set -a; source scripts/dd-fulfillment/openrouter.env; set +a
export PLANNER=compat                                        # runners default to glm; compat is explicit
export PLANNER_BASE_URL="https://openrouter.ai/api/v1"       # or Groq/Gemini/Cerebras/self-hosted
export PLANNER_MODEL="nvidia/nemotron-3-ultra-550b-a55b:free"
RUNS=10 node run-spike.mjs     # text mode    |  node som-demo.mjs  # visual mode
```

Switching providers = changing those variables. No code changes. Guard (review-mode write blocking), audit JSONL, and screenshots work identically on every provider.

## Verification trail

- OpenRouter key: `is_free_tier: true`, usage 0, free daily limit 50 (live via `/api/v1/key`)
- compat text planner (`PLANNER=compat`, Nemotron 550B `:free`): DENIED + CO-97 exact, 3 steps, 41.7 s, ~3,350 tok
- compat visual mode (Nemotron VL `:free`): marks identified 3/3, full task **exact match**, ~3,461 tok, $0.00
- GLM planner: 10/10 spike + 5/5 batch (correctly attributed as of v2 of this guide)
