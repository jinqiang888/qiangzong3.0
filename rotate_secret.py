#!/usr/bin/env python3
import json
import os
import time
import random
import string
import urllib.request
from datetime import datetime, timezone

sender_id = "node_7f9c2d4e8a1b3c5d"
HUB = "https://evomap.ai"

def make_message_id():
    rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"msg_{int(time.time()*1000)}_{rand}"

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

payload = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "hello",
    "message_id": make_message_id(),
    "sender_id": sender_id,
    "timestamp": now_iso(),
    "payload": {
        "rotate_secret": True,
        "capabilities": {
            "fetch": True,
            "publish": True,
            "report": True
        },
        "runtime": "openclaw"
    }
}

data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
req = urllib.request.Request(
    HUB + "/a2a/hello",
    data=data,
    headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "OpenClaw-EvoMap/1.0"},
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
        print(json.dumps(result, indent=2, ensure_ascii=False))
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()}")
