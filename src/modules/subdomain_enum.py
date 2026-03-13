import dns.resolver
import socket
from concurrent.futures import ThreadPoolExecutor
from core.logger import Logger

def check_subdomain(subdomain):
    result = {"subdomain": subdomain, "ip": None, "cname": None}
    try:
        # Get IP
        result["ip"] = socket.gethostbyname(subdomain)
        
        # Try to get CNAME for takeover hints
        try:
            answers = dns.resolver.resolve(subdomain, 'CNAME')
            for rdata in answers:
                result["cname"] = str(rdata.target)
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            pass
            
        return result
    except socket.gaierror:
        return None

def run(domain, wordlist_path, threads=10):
    Logger.run(f"Running Subdomain enumeration for {domain} using {wordlist_path}")
    subdomains_found = []
    
    try:
        with open(wordlist_path, 'r') as f:
            words = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        Logger.error(f"Wordlist not found: {wordlist_path}")
        return subdomains_found

    targets = list(set([f"{word}.{domain}" for word in words]))
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(check_subdomain, targets)
        
    for res in results:
        if res:
            subdomains_found.append(res)
            
    Logger.success(f"Found {len(subdomains_found)} subdomains")
    return subdomains_found
