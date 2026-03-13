import requests
from concurrent.futures import ThreadPoolExecutor
from core.logger import Logger

def check_dir(url):
    try:
        response = requests.get(url, timeout=3, allow_redirects=False)
        if response.status_code in [200, 301, 302, 401, 403]:
            return {"url": url, "status": response.status_code}
    except requests.RequestException:
        pass
    return None

def run(domain, wordlist_path, threads=10):
    Logger.run(f"Running Directory Discovery for {domain} using {wordlist_path}")
    discovered_dirs = []
    
    try:
        with open(wordlist_path, 'r') as f:
            words = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        Logger.error(f"Wordlist not found: {wordlist_path}")
        return discovered_dirs

    base_url = f"http://{domain}"
    targets = [f"{base_url}/{word}" for word in words]
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(check_dir, targets)
        
    for res in results:
        if res:
            discovered_dirs.append(res)
            
    Logger.success(f"Discovered {len(discovered_dirs)} directories/files")
    return discovered_dirs
