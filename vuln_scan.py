import subprocess

def run_nmap_scan(target):
    try:
        result = subprocess.run(
            [
                "nmap",
                "-p", "21,22,23,80,443,445",
                "--script", "ftp-vsftpd-backdoor,http-vuln-cve2015-1635",
                target
            ],
            capture_output=True,
            text=True,
            timeout=200
        )
        return result.stdout if result.stdout else "No known vulnerabilities found."
    except subprocess.TimeoutExpired:
        return "⚠ Nmap scan timed out."
    except Exception as e:
        return f"❌ Vulnerability scan failed: {str(e)}"

def run_nmap_custom(target, scan_flag):
    try:
        result = subprocess.run(
            ["nmap", scan_flag, target],
            capture_output=True,
            text=True,
            timeout=200
        )
        return result.stdout if result.stdout else "No output received."
    except subprocess.TimeoutExpired:
        return "⚠ Nmap custom scan timed out."
    except Exception as e:
        return f"❌ Custom scan failed: {str(e)}"
