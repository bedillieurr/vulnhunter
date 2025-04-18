import requests

def check(url):
    try:
        r = requests.get(url, timeout=5)
        csp = r.headers.get("Content-Security-Policy")
        if csp:
            print(f"[+] CSP found: {csp}")
            if "unsafe-inline" in csp or "unsafe-eval" in csp:
                print("[!] CSP contains unsafe policies!")
        else:
            print("[!] No CSP header found.")
    except Exception as e:
        print(f"[x] CSP check failed: {e}")
