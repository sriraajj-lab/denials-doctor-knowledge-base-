#!/usr/bin/env python3
"""Test alternate Qwen models on the existing MaaS endpoint (runs on droplet)."""
import json
import urllib.request

KEY = [l.split("=", 1)[1].strip() for l in open("/etc/denials-doctor/env") if l.startswith("QWEN_API_KEY=")][0]
BASE = [l.split("=", 1)[1].strip() for l in open("/etc/denials-doctor/env") if l.startswith("QWEN_BASE_URL=")][0]
MODELS = ["qwen-max", "qwen-plus", "qwen-turbo", "qwen-flash", "qwen2.5-72b-instruct"]

for model in MODELS:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "Reply with the single word: ok"}],
        "max_tokens": 8,
    }).encode()
    req = urllib.request.Request(BASE + "/chat/completions", data=body, headers={
        "Authorization": "Bearer " + KEY, "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode())
        text = (d.get("choices") or [{}])[0].get("message", {}).get("content", "")
        print(f"{model}: OK -> {text.strip()[:40]!r}")
    except Exception as e:
        msg = ""
        if hasattr(e, "read"):
            try:
                msg = e.read().decode()[:120]
            except Exception:
                pass
        print(f"{model}: FAIL {type(e).__name__} {msg}")
