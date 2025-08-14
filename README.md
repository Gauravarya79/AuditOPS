# AuditOPS
smart auditing operations
# 🛡️ Cybersecurity Vulnerability Scanner & Home Network Auditor

A **Python + Flask** based cybersecurity toolkit that helps security professionals and students **scan, audit, and harden networks**.  
It combines **traditional Nmap scans** with a **custom home network audit module** for detecting device exposure, open ports, and security risks in LAN environments.

---


---

## 🔍 Overview

Modern networks face constant threats from open ports, unpatched services, and insecure configurations.  
This toolkit is designed for **penetration testers, ethical hackers, and network administrators** to:

- Map active devices in the network.
- Identify open ports and exposed services.
- Detect known vulnerabilities using **CVE checks**.
- Audit home networks for IoT & smart device risks.

It has been **tested on Kali Linux** but can work on other Linux distributions.

---

## ✨ Features

### **Scanning Modes**
- **Port Scan:** Basic TCP/UDP open port check.
- **SYN Scan:** Fast, stealthy half-open scan.
- **Aggressive Scan:** OS fingerprinting + service detection.
- **Vulnerability Scan:** Uses Nmap scripts to detect known CVEs.
- **Home Network Audit:** Identifies devices in local subnet and checks security posture.

### **Home Network Audit Special Abilities**
- Detects IoT devices (CCTV, smart TVs, etc.).
- Highlights insecure services (FTP, Telnet, HTTP without SSL).
- Lists devices by MAC address & vendor (when available).
- Supports an **Ignore List** for NAT/loopback IPs.

---

## 🛠 Tech Stack

| Layer        | Technology |
|--------------|------------|
| **Backend**  | Python 3, Flask |
| **Scanning** | Nmap (via `python-nmap` & subprocess) |
| **UI**       | HTML, CSS (Flask templates) |
| **OS**       | Linux (tested on Kali) |

---

## ⚙️ How It Works

1. **Flask Web UI**  
   The user selects scan type & target from a simple web dashboard.

2. **Nmap Command Execution**  
   Based on scan type, the backend runs different Nmap commands:
   - `nmap -p-` for port scanning.
   - `nmap -sS` for SYN scanning.
   - `nmap -A` for aggressive scans.
   - `nmap --script vuln` for vulnerability detection.

3. **Home Network Audit Process**
   - Detects local subnet (e.g., `192.168.1.0/24`).
   - Uses `nmap -sn` to find active hosts.
   - Filters out ignored IPs (`127.0.0.1`, `10.0.2.2`, etc.).
   - Scans each device for open ports & insecure services.

4. **Result Parsing**  
   Raw Nmap output is parsed into clean, human-readable reports in the web UI.

---

## 📦 Installation

**Prerequisites:**
- Python 3.8+
- Nmap installed (`sudo apt install nmap` on Debian/Ubuntu/Kali)

**Steps:**
```bash
git clone https://github.com/yourusername/projectname.git
cd projectname
pip install -r requirements.txt
