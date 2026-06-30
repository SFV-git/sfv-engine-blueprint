# Dedicated Specifications for Syncthing and Tailscale

---

## **Syncthing Specifications**

### **1. Folders**
- **Configuration**: Each folder is defined with:
  - **Path**: Local directory path on the device.
  - **Encryption**: Optional, with support for AES-256-GCM for end-to-end encryption between devices.
  - **Device Permissions**: Specifies which devices (via device IDs) are allowed to sync the folder (read-only or two-way sync).
  - **Folder ID**: Unique identifier for the folder, used to map across devices.
- **Isolation**: Folders are isolated per device, ensuring that changes in one folder do not affect others.

### **2. Version History**
- **Retention Policy**: 
  - Syncthing retains a limited number of file versions (default: 5) or a time-based retention period (e.g., 30 days).
  - Configurable via the `maxVersions` and `versionRetention` settings in `config.xml`.
- **Storage**: Previous versions are stored in a hidden directory (`.syncthing/versions`) on the device, preserving the original file structure.
- **Access**: Users can manually inspect or restore previous versions through the Syncthing GUI or CLI.

### **3. Conflict Handling**
- **Conflict Detection**: Syncthing detects conflicts when multiple devices modify the same file simultaneously.
- **Resolution Strategy**:
  - Creates a conflict file with a timestamp (e.g., `filename (2).txt`) to preserve both versions.
  - Notifies the user via the GUI or logs, requiring manual resolution.
- **Device Priority**: Optional configuration to prioritize a specific device's version during conflicts (e.g., "last writer wins").

---

## **Tailscale Specifications**

### **1. Isolation Rules**
- **Policy Types**:
  - **Tag-Based Rules**: Allow/deny traffic between nodes based on assigned tags (e.g., `@webserver`).
  - **IP Range Rules**: Restrict traffic to specific IP ranges (e.g., `192.168.1.0/24`).
  - **Port/Protocol Rules**: Control access to specific ports (e.g., allow TCP 80/443).
- **Default Behavior**: Isolation is enforced by default; all traffic is blocked unless explicitly allowed.
- **Management**: Configured via the Tailscale CLI, API, or web interface.

### **2. Node IPs**
- **Assignment**:
  - Each node receives a **unique IPv6 address** (e.g., `fd00::1234`) and optionally an IPv4 address via NAT.
  - IPs are managed by Tailscale's control plane, ensuring uniqueness and proper routing.
- **Stability**: IPs remain consistent across restarts unless the node is removed from the network.

### **3. Remote Policy**
- **Centralized Management**:
  - Policies can be updated remotely via the Tailscale web interface or API.
  - Changes propagate to all nodes in the network, ensuring consistent enforcement.
- **Use Cases**: 
  - Blocking unauthorized access to internal services.
  - Enforcing segmentation between teams or departments.

---

## **Resolving INTEGRATIONS.md Contradiction**

### **Contradiction Summary**
The original `INTEGRATIONS.md` document may have conflicting statements, such as:
- Syncthing requiring open ports for peer-to-peer communication.
- Tailscale enforcing strict isolation by default, potentially blocking Syncthing's traffic.

### **Resolution**
1. **Network Compatibility**:
   - **Tailscale Integration**: Syncthing can be configured to use Tailscale's mesh network, eliminating the need for open ports on public interfaces.
   - **Isolation Rules**: Tailscale's isolation rules can be explicitly configured to allow Syncthing traffic (e.g., allowing UDP 22000–22010 for discovery and TCP/UDP for sync).
   - **Example Rule**:
     ```bash
     tailscale setpolicy allow from device=devicex to device=devicex port=22000-22010
     ```

2. **Encryption and Security**:
   - **Syncthing**: Uses end-to-end encryption for file data.
   - **Tailscale**: Encrypts all network traffic between nodes.
   - **Compatibility**: Both use encryption, but for different layers (data vs. network). They can coexist without conflict.

3. **Version History & Conflict Handling**:
   - Syncthing's version history and conflict resolution are independent of Tailscale and do not interfere with network policies.
   - Tailscale's remote policy can be used to restrict access to Syncthing's sync endpoints, ensuring only authorized nodes can participate.

4. **Documentation Update**:
   - Clarify that Tailscale's isolation rules must be explicitly configured to allow Syncthing's required ports.
   - Emphasize that Syncthing's folder and version history settings are device-specific and do not affect Tailscale's network policies.

---

## **Conclusion**
- **Syncthing** provides robust file sync with version history and conflict resolution.
- **Tailscale** ensures secure, isolated networking with remote policy management.
- **Integration**: When used together, Tailscale's isolation rules must be configured to permit Syncthing's traffic, ensuring seamless operation without security compromises.