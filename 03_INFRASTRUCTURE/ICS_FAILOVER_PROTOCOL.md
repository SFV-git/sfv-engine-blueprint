### ICS-Internet Failover Protocol for Roles 4 and 5  
*(Engine Body: ICS Host; R&D External Calls: External Research & Development Services)*  

---

#### **1. Overview**  
This protocol defines failover logic for **Roles 4 and 5** in an ICS (Industrial Control System) environment, ensuring continuity during:  
- **Engine Body (ICS Host)** downtime  
- **R&D external call stalls** (e.g., API timeouts, network congestion, or service unavailability)  

**Key Objectives**:  
- **Buffer** data during outages to prevent loss.  
- **Retry** failed operations with exponential backoff.  
- **Gracefully degrade** system functionality to maintain critical operations.  

---

#### **2. Failover Protocol for Roles 4 and 5**  
**Roles**:  
- **Role 4**: Primary data processing and control logic.  
- **Role 5**: Secondary redundancy node, backup for Role 4, and R&D interface manager.  

**Failover States**:  
1. **Normal Operation**:  
   - Role 4 communicates with Engine Body and R&D services.  
   - Role 5 remains in standby, monitoring health of Role 4 and Engine Body.  

2. **Failover Triggered (Engine Body Offline)**:  
   - Role 4 detects Engine Body unavailability (via heartbeat timeouts, API errors).  
   - Role 5 assumes control of non-critical functions (e.g., logging, data aggregation).  

3. **Failover Active**:  
   - Role 4 enters **degraded mode**, buffering data locally.  
   - Role 5 routes R&D calls through a **failover proxy** (if available) or applies degradation rules.  

4. **Recovery**:  
   - Engine Body returns online → Role 4 resumes primary duties.  
   - Role 5 flushes buffered data, re-syncs with Engine Body, and reverts to standby.  

---

#### **3. Buffer Logic**  
**Purpose**: Temporarily store data during Engine Body or R&D outages.  

**Implementation**:  
- **Data Buffer**:  
  - Use a **circular queue** with capacity limits (e.g., 1 GB or 10,000 entries).  
  - Prioritize **critical control data** (e.g., safety alarms, process parameters) over non-critical data (e.g., logs, diagnostics).  
  - Timestamp entries for FIFO (First-In-First-Out) or priority-based eviction.  

- **R&D Call Buffer**:  
  - Store stalled R&D requests (e.g., API calls) in a **dedicated queue**.  
  - If buffer is full, drop **non-essential R&D calls** (e.g., analytics, updates) to preserve critical data.  

**Example**:  
```plaintext
Buffer: [Critical_Control_Data, R&D_Request_1, R&D_Request_2, ...]  
Max Capacity: 10,000 entries  
Priority: Critical_Control_Data > R&D_Request  
```

---

#### **4. Retry Logic**  
**Purpose**: Re-establish communication with Engine Body or R&D services after failures.  

**Rules**:  
- **Exponential Backoff**:  
  - Retry intervals: 1s, 2s, 4s, 8s, 16s (max 30s).  
  - Cap retries at **5 attempts** for Engine Body; **3 attempts** for R&D calls.  

- **Retry Triggers**:  
  - **Engine Body**: Heartbeat timeout (e.g., >10s no response).  
  - **R&D Calls**: API timeout (>5s) or HTTP 5xx errors.  

- **Retry Scope**:  
  - Role 4: Reconnect to Engine Body.  
  - Role 5: Re-attempt R&D calls using buffered requests.  

**Example**:  
```plaintext
Attempt 1: Retry in 1s  
Attempt 2: Retry in 2s  
...  
Attempt 5: If failed, trigger graceful degradation.  
```

---

#### **5. Graceful Degradation Logic**  
**Purpose**: Maintain minimal operational functionality during outages.  

**Rules**:  
- **Engine Body Offline**:  
  - **Role 4**:  
    - Disable non-critical functions (e.g., user interface, non-essential sensors).  
    - Use **local cached data** for control decisions (e.g., fallback setpoints).  
  - **Role 5**:  
    - Route R&D calls to **offline mode**:  
      - Return cached responses or default values (e.g., "Service Unavailable").  
      - Log errors for later reconciliation.  

- **R&D Call Stall**:  
  - **Role 4**:  
    - Skip non-critical R&D tasks (e.g., software updates, diagnostics).  
    - Continue processing control logic with last-known R&D data.  
  - **Role 5**:  
    - Redirect R&D calls to **local proxy** (if available) or delay execution.  

**Degradation Thresholds**:  
- Engine Body offline > 5 minutes → Full degradation (manual intervention required).  
- R&D stall > 10 minutes → Disable all R&D-related features.  

---

#### **6. Handling R&D External Call Stalls**  
**Detection**:  
- Use **heartbeat checks** (e.g., every 30s) and **timeout thresholds** (e.g., 5s for API calls).  

**Actions**:  
1. **Stall Detected**:  
   - Buffer R&D call in Role 4/5.  
   - Retry using exponential backoff (see Section 4).  

2. **Persistent Stall (>5 minutes)**:  
   - Role 4: Use **cached R&D data** (e.g., last successful response) for control decisions.  
   - Role 5: Disable R&D features and notify operators via **alert system**.  

3. **Recovery**:  
   - Once R&D service resumes, flush buffer and retry stalled calls.  

---

#### **7. Monitoring and Recovery**  
**Monitoring**:  
- **Heartbeat Checks**:  
  - Engine Body: Every 10s (Role 4/5).  
  - R&D Services: Every 30s (Role 5).  
- **Metrics Tracked**:  
  - Buffer occupancy, retry counts, degradation triggers.  

**Recovery Actions**:  
- **Automated Recovery**:  
  - If Engine Body returns online, Role 4 resumes control; Role 5 flushes buffer.  
- **Manual Recovery**:  
  - For persistent outages, operators must intervene (e.g., reboot Engine Body, restart R&D services).  

---

#### **8. Example Scenario**  
**Scenario**: Engine Body crashes, R&D API stalls.  
**Steps**:  
1. Role 4 detects Engine Body offline → buffers control data.  
2. Role 5 takes over R&D calls, buffers stalled requests.  
3. Role 4 retries Engine Body connection (exponential backoff).  
4. After 5 failed retries, Role 4 degrades to local control using cached data.  
5. Role 5 retries R&D calls; if stalled >10min, disables R&D features.  
6. Engine Body recovers → Role 4 resumes, buffer flushed.  

---

#### **9. Parameters Summary**  
| Parameter               | Value                          |  
|------------------------|--------------------------------|  
| Buffer Capacity        | 1 GB or 10,000 entries         |  
| Retry Interval (Engine Body) | 1s, 2s, 4s, 8s, 16s (max 30s) |  
| Retry Interval (R&D)   | 1s, 2s, 4s (max 8s)            |  
| Degradation Threshold  | Engine Body: 5 min; R&D: 10 min |  
| Graceful Degradation   | Local control, cached data, alerting |  

--- 

This protocol ensures minimal disruption during outages while maintaining safety and operational continuity in ICS environments.