import requests

def audit(url):
    print(f"[*] Auditing SSL and HTTP headers on: {url}")
    try:
        r = requests.get(url, timeout=5, verify=False)
        for header in ["Strict-Transport-Security", "X-Frame-Options", "X-Content-Type-Options", "Content-Security-Policy"]:
            if header in r.headers:
                print(f"[+] {header}: {r.headers[header]}")
            else:
                print(f"[!] Missing {header}")
    except Exception as e:
        print(f"[x] Audit failed: {e}")
