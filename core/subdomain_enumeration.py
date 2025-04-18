import requests
import socket

def enumerate(domain, brute_force=False):
    print(f"[*] Enumerating subdomains for {domain}...")
    subdomains = set()

    # crt.sh lookup
    try:
        r = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json")
        if r.ok:
            for entry in r.json():
                sub = entry['name_value'].split('\n')[0]
                if domain in sub:
                    subdomains.add(sub.strip())
    except Exception as e:
        print(f"[!] crt.sh error: {e}")

    # Brute force (optional)
    if brute_force:
        print("[*] Performing DNS brute-force...")
        with open("wordlist.txt") as f:
            for line in f:
                sub = f"{line.strip()}.{domain}"
                try:
                    socket.gethostbyname(sub)
                    subdomains.add(sub)
                except:
                    pass

    for sub in sorted(subdomains):
        print(f"[+] Found subdomain: {sub}")
