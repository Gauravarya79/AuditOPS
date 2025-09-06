  GNU nano 8.4                                         network_monitor.py                                                   
import subprocess
import time
import signal

def get_top_bandwidth_user(duration=10):
    try:
        cmd = ["sudo", "nethogs", "-t"]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Let nethogs run for the given duration
        time.sleep(duration)

        # Gracefully stop it (like Ctrl+C)
        process.send_signal(signal.SIGINT)

        # Now read the output
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()

        usage = {}
        for line in stdout.strip().split("\n"):
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                raw_addr = parts[0].split('/')[0].strip()
                ip = raw_addr if raw_addr and raw_addr != '?' else 'Unknown'
                try:
                    kbps = float(parts[2])
                    usage[ip] = usage.get(ip, 0) + kbps
                except ValueError:
                    continue

        if not usage:
            return "No bandwidth data found."

        top_ip = max(usage, key=usage.get)
        return f"{top_ip} is using the most bandwidth: {usage[top_ip]:.2f} KB/s"

    except Exception as e:
        return f"Error measuring bandwidth: {str(e)}"
 not showing anything



