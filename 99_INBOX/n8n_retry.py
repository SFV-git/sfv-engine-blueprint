import os
import json
import urllib.request
import time

vault = r"C:\SFV_BLUEPRINT"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZTMxNWEwZi02YWI0LTRkODEtYjY1NS05Yzc2MjBhMTY1N2MiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiZmE3ODZjNmMtYTJjMy00M2ZhLWE3ODgtMDgwNDZlYjQ0Yzk5IiwiaWF0IjoxNzgwMDI4NDY4fQ.0T6li5XEFJNbJ_iNNzG3ztiB4u4Gj5S7KC3PM94KgiM"

headers = {
    'Content-Type': 'application/json',
    'X-N8N-API-KEY': api_key
}

wfs = [
    r"C:\SFV_BLUEPRINT\03_INFRASTRUCTURE\n8n_workflows\workflow1_queue_processor.json"
]

print("--- IMPORTING WORKFLOWS ---")
for wf in wfs:
    try:
        with open(wf, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Remove ID to prevent collision if that's the issue
        if 'id' in data:
            del data['id']
        req = urllib.request.Request("http://localhost:5678/api/v1/workflows", 
            data=json.dumps(data).encode('utf-8'),
            headers=headers)
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            print(f"Imported successfully: {res.get('id')}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code}")
        print(e.read().decode())
