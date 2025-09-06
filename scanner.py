import socket
import subprocess

def basic_scan(target):
    open_ports = []
    common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389]
    for port in common_ports:
        try:
            s = socket.socket()
            s.settimeout(1)
            s.connect((target, port))
            open_ports.append(port)
            s.close()
        except:
            pass
    return open_ports

def nmap_vuln_scan(target):
    try:
        # Run safer and faster vulnerability checks
        result = subprocess.run(
            [
                "nmap",
                "-p", "21,22,23,80,443,445",  # only common ports
                "--script", "ftp-vsftpd-backdoor,http-vuln-cve2015-1635,http-dombased-xss",
                target
            ],
            capture_output=True,
            text=True,
            timeout=40
        )
        return result.stdout if result.stdout else "No known vulnerabilities found."
    except subprocess.TimeoutExpired:
        return "⚠ Nmap scan timed out after 30 seconds."
    except Exception as e:
        return f"❌ Scan failed: {str(e)}"

