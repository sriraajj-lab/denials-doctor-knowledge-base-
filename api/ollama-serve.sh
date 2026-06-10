#!/bin/bash
# Denials Doctor - Ollama/vLLM API Serving Configuration
# This script serves the fine-tuned RCM LLM via Ollama for client API access

# === Option 1: Ollama (easiest, good for testing) ===
# Prerequisites: Install Ollama from https://ollama.com

# Create the model from the knowledge base files
ollama create denials-doctor-rcm -f - <<'MODELFILE'
FROM phi-4:14b  # or llama3.2:8b

# Set system prompt for RCM expertise
SYSTEM """You are Denials Doctor, an AI assistant specialized in healthcare Revenue Cycle Management (RCM) and Electronic Health Records (EHR) integration.

You can answer questions about:
- Medical coding (CPT, ICD-10, HCPCS, modifiers)
- Insurance eligibility and benefits verification
- Claim submission and EDI transactions (837, 835, 270/271, 278)
- Denial management and appeals (all levels)
- Payment posting and reconciliation
- EHR integration (FHIR R4, HL7 v2, X12 EDI)
- HIPAA compliance and audit readiness
- Provider credentialing and enrollment
- Prior authorization requirements

Provide detailed, accurate answers with specific codes, timeframes, and regulations when applicable. Always note that regulations may vary by payer and jurisdiction."""

# Set parameters
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_ctx 8192
MODELFILE

# Serve the model
ollama serve

# ---
# === Option 2: vLLM (production, good for high throughput) ===
# Prerequisites: pip install vllm

# python -m vllm.entrypoints.openai.api_server \
#     --model path/to/fine-tuned-model \
#     --task generate \
#     --trust-remote-code \
#     --dtype auto \
#     --max-model-len 8192 \
#     --api-key denials-doctor-secret

# === Client API Usage ===
# curl -X POST http://localhost:11434/api/generate \
#   -H "Content-Type: application/json" \
#   -d '{
#     "model": "denials-doctor-rcm",
#     "prompt": "How do I appeal a Medicare medical necessity denial?",
#     "stream": false
#   }'