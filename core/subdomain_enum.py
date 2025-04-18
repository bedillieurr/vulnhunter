import requests
import dns.resolver
import os
from concurrent.futures import ThreadPoolExecutor

def get_subdomains_from_crtsh(domain):
    print(f"[+] Fetching subdomains from crt.sh for: {domain}")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            print(f"[-] Error fetching from crt.sh")
            return []

        data = r.json()
        subdomains = set()
        for entry in data:
            name = entry['name_value']
            for sub in name.split('\n'):
                if domain in sub:
                    subdomains.add(sub.strip())
        return list(subdomains)
    except Exception as e:
        print(f"[-] Exception during crt.sh request: {e}")
        return []

def is_domain_active(domain):
    try:
        dns.resolver.resolve(domain, 'A')
        return True
    except:
        return False

def filter_active_subdomains(subdomains, threads=10):
    print("[+] Checking for active subdomains...")
    active = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(lambda d: (d, is_domain_active(d)), subdomains)
        for domain, status in results:
            if status:
                active.append(domain)
    return active

def enumerate_active_subdomains(domain):
    raw_subs = get_subdomains_from_crtsh(domain)
    active_subs = filter_active_subdomains(raw_subs)
    return active_subs
    
def brute_force_subdomains(domain, wordlist_path="wordlists/subdomains.txt", threads=10):
    print(f"[+] Bruteforcing subdomains for: {domain}")
    if not os.path.exists(wordlist_path):
        print(f"[-] Wordlist not found at: {wordlist_path}")
        return []

    with open(wordlist_path, 'r') as f:
        words = [line.strip() for line in f if line.strip()]
    
    brute_targets = [f"{word}.{domain}" for word in words]
    active_subs = filter_active_subdomains(brute_targets, threads=threads)
    return active_subs

def enumerate_active_subdomains(domain):
    crtsh_subs = get_subdomains_from_crtsh(domain)
    brute_subs = brute_force_subdomains(domain)

    combined = set(crtsh_subs + brute_subs)
    active = filter_active_subdomains(combined)
    return active
