$body = '{"model":"qwen3:14b","keep_alive":0}'
Invoke-RestMethod -Uri "http://localhost:11434/api/generate" -Method POST -ContentType "application/json" -Body $body
Write-Output "qwen3 keepalive released"
