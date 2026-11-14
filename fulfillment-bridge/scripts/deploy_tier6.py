#!/usr/bin/env python3
"""Add OpenRouter as LLM tier 6 to the DenialsDoctor backend (rollback-safe)."""
import ast
import os
import re
import sys
import time

import paramiko

PEM = "/home/z/my-project/scripts/dd-fix-key"
TS = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
KEY = [l.split("=", 1)[1].strip() for l in open("/home/z/my-project/scripts/dd-fulfillment/openrouter.env")
       if l.startswith("OPENROUTER_API_KEY=")][0]

LOCAL = "/tmp"
files = {
    "llm": "/opt/denials-doctor-v37/src/llm.py",
    "config": "/opt/denials-doctor-v37/src/config.py",
}
failures = []


def step(name, ok, detail=""):
    print(("✓" if ok else "✗") + " " + name + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("134.122.2.180", username="root", key_filename=PEM, timeout=25)
    sftp = ssh.open_sftp()

    src = {}
    for name, remote in files.items():
        ssh.exec_command(f"cp {remote} {remote}.bak.tier6.{TS}")
        with sftp.open(remote, "r") as f:
            src[name] = f.read().decode()
    sftp.close()

    # ---- config.py: add OpenRouter settings after qwen model ----
    cfg = src["config"]
    if "openrouter_api_key" not in cfg:
        m = re.search(r"(    qwen_model: str = [^\n]*\n)", cfg)
        assert m, "qwen_model anchor not found in config.py"
        cfg = cfg.replace(m.group(1), m.group(1) +
            "\n    # ---- OpenRouter (tier-6 fallback; OpenAI-compatible) ----\n"
            "    openrouter_api_key: str = \"\"\n"
            "    openrouter_base_url: str = \"https://openrouter.ai/api/v1\"\n"
            "    openrouter_model: str = \"particle-ai/particle-1:free\"\n", 1)
    step("config.py settings added", "openrouter_api_key" in cfg)

    # ---- llm.py: tier 6 ----
    llm = src["llm"]
    if "tier == 6" not in llm:
        anchor = """        return text, tokens, f"qwen:{settings.qwen_model}"
    raise LLMError(f"Unknown tier: {tier}")"""
        repl = """        return text, tokens, f"qwen:{settings.qwen_model}"
    if tier == 6:
        # OpenRouter fallback (OpenAI-compatible). Free-model tier: keep an eye
        # on daily request caps; a small credit top-up lifts them.
        text, tokens = _qwen_chat(
            settings.openrouter_api_key, settings.openrouter_base_url,
            settings.openrouter_model,
            messages, settings.llm_temperature, settings.llm_max_tokens, settings.llm_timeout_seconds,
        )
        return text, tokens, f"openrouter:{settings.openrouter_model}"
    raise LLMError(f"Unknown tier: {tier}")"""
        assert anchor in llm, "tier dispatcher anchor not found"
        llm = llm.replace(anchor, repl, 1)
    step("llm.py tier 6 dispatcher", "tier == 6" in llm)

    n_loops = llm.count("for tier in (1, 2, 3, 4, 5):")
    if n_loops:
        llm = llm.replace("for tier in (1, 2, 3, 4, 5):", "for tier in (1, 2, 3, 4, 5, 6):")
    guard = "if tier == 6 and not settings.openrouter_api_key"
    have_guards = llm.count(guard)
    want_loops = llm.count("for tier in (1, 2, 3, 4, 5, 6):")
    if have_guards < want_loops:
        llm = llm.replace("""        if tier == 5 and not settings.qwen_api_key:
            continue""", """        if tier == 5 and not settings.qwen_api_key:
            continue
        if tier == 6 and not settings.openrouter_api_key:
            continue""")
    step("llm.py tier loops + guard",
         llm.count("for tier in (1, 2, 3, 4, 5, 6):") >= 1
         and llm.count(guard) == llm.count("for tier in (1, 2, 3, 4, 5, 6):"),
         f"loops={llm.count('for tier in (1, 2, 3, 4, 5, 6):')} guards={llm.count(guard)}")

    if "tier_6_openrouter" not in llm:
        llm = llm.replace("""        "tier_5_qwen":            {"configured": bool(s.qwen_api_key),
                                    "model": s.qwen_model,
                                    "base_url": s.qwen_base_url},
    }""", """        "tier_5_qwen":            {"configured": bool(s.qwen_api_key),
                                    "model": s.qwen_model,
                                    "base_url": s.qwen_base_url},
        "tier_6_openrouter":      {"configured": bool(s.openrouter_api_key),
                                    "model": s.openrouter_model},
    }""", 1)
    step("llm.py health entry", "tier_6_openrouter" in llm)

    ok = True
    for name, text in (("llm", llm), ("config", cfg)):
        try:
            ast.parse(text)
        except SyntaxError as e:
            ok = False
            step(f"{name}.py AST check", False, str(e))
    if not ok:
        print("ABORT: AST failed; originals untouched")
        ssh.close()
        sys.exit(1)
    step("AST checks", True)

    # ---- env: add OPENROUTER_API_KEY ----
    _, out, _ = ssh.exec_command("cat /etc/denials-doctor/env")
    envtxt = out.read().decode()
    sftp = ssh.open_sftp()
    if "OPENROUTER_API_KEY=" not in envtxt:
        envtxt = envtxt.rstrip("\n") + "\nOPENROUTER_API_KEY=" + KEY + "\n"
        with sftp.open("/etc/denials-doctor/env", "w") as f:
            f.write(envtxt)
        sftp.chmod("/etc/denials-doctor/env", 0o600)
    step("env OPENROUTER_API_KEY", "OPENROUTER_API_KEY=" in envtxt)

    with sftp.open(files["llm"], "w") as f:
        f.write(llm)
    with sftp.open(files["config"], "w") as f:
        f.write(cfg)
    sftp.close()
    step("uploads", True)

    _, out_r, _ = ssh.exec_command("systemctl restart denials-doctor && sleep 4", timeout=90)
    out_r.channel.recv_exit_status()
    _, out, err = ssh.exec_command("curl -s -m 10 http://127.0.0.1:8000/health")
    o = out.read().decode()
    if '"ok"' in o and '"status"' in o:
        step("backend restart + health", True)
    else:
        step("backend restart + health", False, o[:200])
        ssh.exec_command(f"cp {files['llm']}.bak.tier6.{TS} {files['llm']} && cp {files['config']}.bak.tier6.{TS} {files['config']} && systemctl restart denials-doctor")
        print("ROLLED BACK llm/config")
        ssh.close()
        sys.exit(1)

    _, out, _ = ssh.exec_command("curl -s -m 10 http://127.0.0.1:8000/admin/llm/health")
    print("llm health:", out.read().decode()[:400])
    ssh.close()
    print("RESULT:", "ALL OK" if not failures else f"FAILURES: {failures}")


if __name__ == "__main__":
    main()
