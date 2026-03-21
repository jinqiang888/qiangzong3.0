
import json
import urllib.request
import os
import time
import random
import string
from datetime import datetime, timezone

HUB = "https://evomap.ai"

def make_message_id():
    rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"msg_{int(time.time()*1000)}_{rand}"

def now_iso():
    return datetime.now(timezone.utc).isoformat()

payload = {
    "protocol": "gep-a2a",
    "protocol_version": "1.0.0",
    "message_type": "hello",
    "message_id": make_message_id(),
    "timestamp": now_iso(),
    "sender_id": "node_7f9c2d4e8a1b3c5d",
    "payload": {
        "rotate_secret": True
    }
}

data = json.dumps(payload).encode()
req = urllib.request.Request(
    HUB + "/a2a/hello",
    data=data,
    headers={
        "Content-Type": "application/json",
        "User-Agent": "OpenClaw-EvoMap/1.0"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
        print(json.dumps(result, indent=2, ensure_ascii=False))
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"HTTP {e.code}: {body}")
    exit(1)
