                                                                                                                                                                         
from flask import Flask, request, render_template
from datetime import datetime
from scanner.port_scan import run_port_scan
from scanner.vuln_scan import run_nmap_scan, run_nmap_custom
from scanner.local_audit import run_local_network_audit
import ipaddress
import validators

app = Flask(__name__)
REPORT_FILE = "report.txt"

ALLOWED_SCAN_TYPES = {
    "port", "vuln", "network", "syn", "aggressive", "os", "local_audit"
}

def extract_recent_targets():
    targets = []
    try:
        with open(REPORT_FILE, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("Target:"):
                    target = line.split(":", 1)[1].strip()
                    if target != "Local Network" and target not in targets:
                        targets.append(target)
    except FileNotFoundError:
        pass
    return targets

def is_valid_target(target):
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        return validators.domain(target)  # Checks for valid domain

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    vuln = None

    if request.method == "POST":
        target = request.form.get("target", "").strip()
        scan_type = request.form.get("scan_type", "")

        # ✅ Validate scan_type
        if scan_type not in ALLOWED_SCAN_TYPES:
            return render_template("index.html", result=None, vuln="⚠ Invalid scan type selected.", recent_scans=extract_recent_targets())

        # ✅ Validate target unless it's a local audit
        if scan_type != "local_audit" and not is_valid_target(target):
            return render_template("index.html", result=None, vuln="⚠ Invalid target (must be IP or domain).", recent_scans=extract_recent_targets())

        # ✅ Perform the scan
        try:
            if scan_type == "port":
                result = run_port_scan(target)
            elif scan_type == "vuln":
                vuln = run_nmap_scan(target)
            elif scan_type == "network":
                result = run_nmap_custom(target, "-sn")
            elif scan_type == "syn":
                result = run_nmap_custom(target, "-sS")
            elif scan_type == "aggressive":
                result = run_nmap_custom(target, "-A")
            elif scan_type == "os":
                result = run_nmap_custom(target, "-O")
            elif scan_type == "local_audit":
                vuln = run_local_network_audit()
        except Exception as e:
            vuln = f"⚠ Error occurred during scan: {str(e)}"

        # ✅ Log results
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(REPORT_FILE, "a") as f:
            f.write(f"\n[{timestamp}]\n")
            f.write(f"Target: {target if target else 'Local Network'}\n")
            f.write(f"Type: {scan_type}\n")
            f.write("Result:\n")
            f.write(result or vuln or "No output.")
            f.write("\n" + "-" * 60 + "\n")

    recent_scans = extract_recent_targets()
    return render_template("index.html", result=result, vuln=vuln, recent_scans=recent_scans)

if __name__ == "__main__":
    app.run(debug=True)










