import urllib.request, json
payload = json.dumps({"model":"devstral-small-2","prompt":"Reply only with the exact text: DEVSTRAL_OK","stream":False,"options":{"num_predict":15,"temperature":0}}).encode()
req = urllib.request.Request("http://localhost:11434/api/generate", data=payload, headers={"Content-Type":"application/json"}, method="POST")
with urllib.request.urlopen(req, timeout=120) as r:
    print(json.loads(r.read())["response"].strip())
