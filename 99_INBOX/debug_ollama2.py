import urllib.request, json

content = open(r"C:\SFV_BLUEPRINT\README.md", encoding="utf-8").read()[:400]

# Test 1: /api/chat endpoint instead of /api/generate
payload = json.dumps({
    "model": "qwen3:14b",
    "messages": [
        {"role": "system", "content": "You are a document auditor. Respond ONLY with valid JSON, nothing else. No thinking, no explanation."},
        {"role": "user", "content": (
            "Score this document 1-5:\n"
            "1=generic AI slop 2=major gaps 3=right direction 4=solid 5=complete\n"
            "Respond ONLY with: {\"score\": N, \"summary\": \"one sentence\", \"verdict\": \"one sentence\"}\n\n"
            "Path: README.md\nContent:\n" + content.replace('"', "'")
        )}
    ],
    "stream": False,
    "options": {"temperature": 0.1, "num_predict": 200}
}).encode("utf-8")

req = urllib.request.Request(
    "http://localhost:11434/api/chat",
    data=payload, headers={"Content-Type": "application/json"}, method="POST"
)
with urllib.request.urlopen(req, timeout=90) as r:
    resp = json.loads(r.read())
    raw = resp.get("message", {}).get("content", "")
    print("=== RAW CHAT RESPONSE ===")
    print(repr(raw))
    print()
    # Try to extract JSON
    if "<think>" in raw:
        after = raw.split("</think>")[-1].strip()
    else:
        after = raw.strip()
    print("=== AFTER THINK STRIP ===")
    print(repr(after))
    start = after.find("{")
    end = after.rfind("}") + 1
    if start >= 0 and end > start:
        print("=== PARSED JSON ===")
        print(json.loads(after[start:end]))
    else:
        print("NO JSON FOUND")
