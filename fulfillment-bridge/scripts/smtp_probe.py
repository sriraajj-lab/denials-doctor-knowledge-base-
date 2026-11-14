#!/usr/bin/env python3
"""Probe which SMTP egress path works from this droplet (no credentials printed)."""
import socket
import ssl
import smtplib

HOSTS = ["smtp.zoho.in", "smtp.zoho.com"]
PORTS = [465, 587, 25]

for h in HOSTS:
    try:
        ips = socket.getaddrinfo(h, None)
        print(f"DNS {h}: OK ({ips[0][4][0]})")
    except Exception as e:
        print(f"DNS {h}: FAIL {e}")
        continue
    for p in PORTS:
        try:
            s = socket.create_connection((h, p), timeout=8)
            print(f"TCP {h}:{p} OPEN")
            if p == 465:
                try:
                    with smtplib.SMTP_SSL(h, p, timeout=12, context=ssl.create_default_context()) as sm:
                        print(f"  SMTP_SSL banner: {sm.noop()}")
                except Exception as e:
                    print(f"  SMTP_SSL failed: {type(e).__name__}: {e}")
            s.close()
        except Exception as e:
            print(f"TCP {h}:{p} blocked/timeout ({type(e).__name__})")
