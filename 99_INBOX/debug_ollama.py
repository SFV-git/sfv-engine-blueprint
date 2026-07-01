import urllib.request, json

content = open(r"C:\SFV_BLUEPRINT\README.md", encoding="utf-8").read()[:400]
prompt = (
    "Score this document 1-5:\n"
    "1=generic AI slop 2=major gaps 3=right direction 4=solid 5=complete\n"
    "Respond ONLY with JSON: {\"score\": N, \"summary\": \"...\", \"verdict\": \"...\"}\n\n"
    "Path: README.md\n"
    "Content:\n" + content.replace('"', "'")
)
payload = json.dumps({
    "model": "qwen3:14b",
    "prompt": prompt,
    "stream": False,
    "options": {"temperature": 0.1, "num_predict": 150}
}).encode("utf-8")

req = urllib.request.Request(
    "http://localhost:11434/api/generate",
    data=payload, headers={"Content-Type": "application/json"}, method="POST"
)
with urllib.request.urlopen(req, timeout=60) as r:
    raw = json.loads(r.read())["response"]
    print("=== RAW RESPONSE ===")
    print(repr(raw))
