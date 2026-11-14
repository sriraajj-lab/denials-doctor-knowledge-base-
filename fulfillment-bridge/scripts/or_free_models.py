#!/usr/bin/env python3
"""Find currently-live :free models on OpenRouter and test the top candidates."""
import json
import urllib.request

KEY = [l.split("=", 1)[1].strip() for l in open("/tmp/or_test.env") if l.startswith("OPENROUTER_API_KEY=")][0]

req = urllib.request.Request("https://openrouter.ai/api/v1/models", headers={"Authorization": "Bearer " + KEY})
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.loads(r.read().decode())
free = [m for m in data["data"] if m["id"].endswith(":free")]
free.sort(key=lambda m: -(m.get("context_length") or 0))
print(f"live free models: {len(free)}")
for m in free[:10]:
    print(" ", m["id"], "| ctx:", m.get("context_length"))

for m in [x for x in free if 'thinkingmachines' not in x['id'] and 'gemma' not in x['id'] and 'north-mini' not in x['id']][:6] + [x for x in free if 'gemma' in x['id']][:1]:
    model = m["id"]
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "Reply with the single word: ok"}],
        "max_tokens": 10,
    }).encode()
    r2 = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=body, headers={
        "Authorization": "Bearer " + KEY,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://denialsdoctor.com",
        "X-Title": "DenialsDoctor",
    }, method="POST")
    try:
        with urllib.request.urlopen(r2, timeout=60) as resp:
            d = json.loads(resp.read().decode())
        if isinstance(d, list):
            d = d[0] if d else {}
        ch = d.get("choices")
        if not ch:
            print(f"TEST {model}: ODD {json.dumps(d)[:220]}")
            continue
        text = ch[0].get("message", {}).get("content", "")
        print(f"TEST {model}: OK -> {text.strip()[:40]!r}")
    except Exception as e:
        msg = ""
        if hasattr(e, "read"):
            try:
                msg = e.read().decode()[:120]
            except Exception:
                pass
        print(f"TEST {model}: FAIL {type(e).__name__} {msg}")
