#smart auditing operationsimport subprocess
import socket

# IPs to ignore (e.g., loopback or virtual NAT IPs)
IGNORED_IPS = {"127.0.0.1", "127.0.1.1", "10.0.2.2", "10.0.2.3", "10.0.2.15"}

def get_subnet_range():
    """
    Determines the local network subnet (e.g., 192.168.1.0/24) using system routing info.
    """
    try:
        route = subprocess.check_output("ip route", shell=True).decode()
        for line in route.splitlines():
            if "src" in line:
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "src":
                        ip = parts[i + 1]
                        subnet = ip.rsplit('.', 1)[0] + ".0/24"
                        return subnet
        return None
    except Exception:
        return None

def run_local_network_audit():
    """
    Scans the local network using Nmap and returns raw-like output with device info
    and highest bandwidth usage.
    """
    try:
        subnet = get_subnet_range()
        if not subnet:
            return "❌ Failed to determine local subnet."

        result = subprocess.run(
            ["nmap", "-sn", subnet],
            capture_output=True,
            text=True,
            timeout=60
        )

        lines = result.stdout.splitlines()
        output = []
        count = 0
        current_ip = ""
        valid_device = False

        for i, line in enumerate(lines):
            if line.startswith("Nmap scan report for"):
                current_ip = line.split()[-1]
                if current_ip not in IGNORED_IPS:
                    valid_device = True
                    output.append(line)
                else:
                    valid_device = False
            elif "Host is up" in line and valid_device:
                output.append(line)
                count += 1
            elif "MAC Address" in line and valid_device:
                output.append(line)

        output.append(f"\n🔍 Total External Devices Detected: {count}")


        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return "⚠ Local network scan failed: Scan timed out after 60 seconds"
    except Exception as e:
        return f"❌ Error: {str(e)}"


