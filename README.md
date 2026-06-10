# Denials Doctor - RCM/EHR Knowledge Base

A comprehensive Revenue Cycle Management (RCM) and Electronic Health Records (EHR) knowledge corpus for training AI agents and small language models in healthcare revenue operations.

## Structure

```
docs/knowledge-base/
├── 01-eligibility-demographics/   Patient demographics, insurance plans, benefits verification
├── 02-medical-coding/             CPT, ICD-10, HCPCS, modifiers, specialty coding
├── 03-claim-scrubbing/            NCCI edits, medical necessity, scrubber logic
├── 04-claim-submission/           EDI 837/835, clearinghouses, payer IDs
├── 05-denial-management/          Denial types, codes, appeals strategy, timely filing
├── 06-prior-authorization/        Auth requirements, EDI 278
├── 07-payment-posting/            EDI 835 posting, payment reconciliation
├── 08-ehr-integration/            FHIR R4, HL7 v2, X12 EDI, EHR systems, agnostic integration
└── 09-operations-compliance/      HIPAA, audit readiness, credentialing

agents/                           Per-agent JSONL training data
├── orchestrator-training.jsonl
├── demographics-agent-training.jsonl
├── eligibility-agent-training.jsonl
├── coding-agent-training.jsonl
├── scrubber-agent-training.jsonl
└── appeals-agent-training.jsonl

training/                         Fine-tuning resources
└── fine-tune-llm.ipynb           Colab notebook for fine-tuning a small LLM

api/                              API serving configuration
└── ollama-serve.sh               Ollama/vLLM serving setup
```

## Usage

### Track A: Agent Training
The per-agent JSONL files in `agents/` contain instruction-tuning format Q&A pairs for each of the 6 Denials Doctor agents. Use these to fine-tune or few-shot prompt each agent.

### Track B: Client-Facing LLM
The entire knowledge corpus is designed to be used as:
1. **RAG reference material** - Chunk the markdown files and ingest into a vector database
2. **Fine-tuning dataset** - Use `training/fine-tune-llm.ipynb` to fine-tune Phi-4, Llama 3.2 8B, or similar
3. **Ollama serve** - Deploy via `api/ollama-serve.sh`

## Content Coverage

- 9 domains across the full RCM lifecycle
- 30+ markdown files with structured clinical and billing knowledge
- 600+ embedded Q&A pairs for agent training
- Real denial codes, CARCs, EDI segments, FHIR resources
- Payer-specific guidance for major US health plans
- EHR integration patterns (Epic, Cerner, Athenahealth, eClinicalWorks)
- HIPAA compliance and audit readiness

## License

Private - Denials Doctor (Aria Agentic Agency)