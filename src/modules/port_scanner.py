import socket
from concurrent.futures import ThreadPoolExecutor
from core.logger import Logger

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]

def scan_port(target_ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            banner = ""
            try:
                # Attempt to grab banner for common services
                if port in [21, 22, 25, 110, 143]:
                    banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
                elif port in [80, 8080]:
                    s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner = s.recv(1024).decode('utf-8', errors='ignore').split('\n')[0].strip()
            except Exception:
                pass
            s.close()
            return {"port": port, "banner": banner}
        s.close()
    except Exception:
        pass
    return None

def run(domain, threads=10):
    Logger.run(f"Running Port Scanner for {domain} on common ports")
    open_ports = []
    
    try:
        target_ip = socket.gethostbyname(domain)
        Logger.info(f"Resolved {domain} to {target_ip}")
    except socket.gaierror:
        Logger.error(f"Failed to resolve {domain}")
        return open_ports

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(scan_port, target_ip, port) for port in COMMON_PORTS]
        
    for f in futures:
        res = f.result()
        if res:
            open_ports.append(res)
            
    Logger.success(f"Found {len(open_ports)} open ports")
    return open_ports
