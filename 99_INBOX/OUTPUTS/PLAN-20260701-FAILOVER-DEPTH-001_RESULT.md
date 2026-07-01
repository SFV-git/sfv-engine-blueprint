# RESULT -- PLAN-20260701-FAILOVER-DEPTH-001

- Executor: ollama
- Status: complete
- Dispatched: 2026-07-01 02:18:06

---

## Node B Failover Behavior

### Detection of Primary Unreachability  
- **Health Check Mechanism**: Implement a periodic heartbeat system where Node B (R&D Terminal) sends a TCP/IP or HTTP-based ping to the primary node (Engine Body) at intervals of 10 seconds. If no response is received for **3 consecutive checks** (totaling 30 seconds), Node B triggers failover logic.  
- **Timeout Threshold**: A 30-second timeout is proposed to balance responsiveness and avoid false positives due to transient network issues.  
- **Graceful Degradation**: During the detection phase, Node B should continue monitoring the primary node and only initiate failover if the timeout is exceeded.  

### Failover to Node B  
- **Service Redirect**: Upon confirming the primary node is unreachable, Node B must **automatically activate its Ollama instance** and redirect all incoming AI requests to its fallback model. This requires pre-configured routing rules in the network stack or a load balancer (e.g., using iptables, HAProxy, or a custom script).  
- **Model Prioritization**: Node B should **preload a lightweight, low-VRAM model** (e.g., `Llama 3 8B` or a 4-bit quantized variant) specifically for failover purposes. This model must be explicitly declared in Ollama’s configuration to prevent accidental loading of larger models that exceed Node B’s VRAM capacity.  
- **Session Persistence**: If possible, maintain session state (e.g., user context, model parameters) through shared storage (e.g., a local file system or Redis) to ensure continuity during failover.  

### Model Selection for Node B  
- **Fallback Model Constraints**: Given VRAM limitations, Node B should use a model with **≤8GB VRAM footprint**. Examples include:  
  - `Llama 3 8B` (with 4-bit quantization)  
  - `Phi-3-mini` (Microsoft)  
  - `Qwen2.5` (Qwen series, small variants)  
- **Preloading**: The fallback model must be **preloaded at Node B startup** to minimize latency during failover. This can be enforced via Ollama’s API with a dedicated `--preload-fallback` flag or a custom init script.  

### Failover Logging and Detection  
- **Event Logging**: Failover events must be logged with **timestamp, cause (e.g., "Primary timeout"), model context, and node status**. Logs should be written to a shared, persistent storage location (e.g., a NAS or cloud bucket) to prevent data loss.  
- **Alerting**: Generate a **system alert** (e.g., via email, Slack, or a local notification daemon) when failover occurs, including details such as the primary node’s last known status and the fallback model loaded on Node B.  
- **Audit Trail**: Maintain an **audit log** that records:  
  - Timestamps of failover initiation and resolution  
  - Models active on both nodes during the event  
  - Any errors encountered during the failover process  
- **Manual Verification**: Include a **post-failover verification step** where Node B checks if the fallback model is running correctly (e.g., via a health check API call to Ollama) and logs the result.  

This design ensures seamless, reliable failover while minimizing resource strain on Node B and providing actionable insights for troubleshooting.
