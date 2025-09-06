import socket

def run_port_scan(target):
    open_ports = []
    common_ports = [21, 22, 23, 80, 443, 445]
    for port in common_ports:
        try:
            sock = socket.socket()
            sock.settimeout(1)
            sock.connect((target, port))
            open_ports.append(port)
            sock.close()
        except:
            pass
    return  f"Open ports:{open_ports}"if open_ports else "No common ports open."

