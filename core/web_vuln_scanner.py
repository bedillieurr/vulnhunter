import requests
from urllib.parse import urljoin

def scan(url, input_file=None):
    print(f"[*] Scanning for web vulnerabilities on {url}")
    try:
        r = requests.get(url, timeout=5, verify=False, allow_redirects=True)
        if "login" in r.url or "admin" in r.url:
            print(f"[!] Possible login/admin panel detected at {r.url}")

        if "Location" in r.headers:
            print(f"[!] Redirects to: {r.headers['Location']}")

        # Basic check for headers
        print("[*] Checking HTTP headers...")
        for header in ["X-Frame-Options", "X-XSS-Protection", "Content-Security-Policy"]:
            if header not in r.headers:
                print(f"[!] Missing header: {header}")

        # SSL info
        if url.startswith("https"):
            print("[*] SSL connection established. Details TBD.")

        # robots.txt
        robots = urljoin(url, "/robots.txt")
        rbt = requests.get(robots)
        if rbt.status_code == 200:
            if "Disallow" in rbt.text:
                print("[!] Sensitive Disallow entries in robots.txt:")
                for line in rbt.text.splitlines():
                    if "Disallow:" in line:
                        print(f"  {line}")

    except Exception as e:
        print(f"[x] Error scanning web target: {e}")
