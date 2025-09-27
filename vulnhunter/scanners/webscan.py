import requests, logging
from bs4 import BeautifulSoup
from ..config import DEFAULT_USER_AGENT

LOG = logging.getLogger("vulnhunter.scanners.webscan")

def _check_headers(resp):
    headers = {k.lower(): v for k, v in resp.headers.items()}
    missing = []
    if "x-frame-options" not in headers:
        missing.append("X-Frame-Options")
    if "content-security-policy" not in headers:
        missing.append("Content-Security-Policy")
    return missing

def _find_login_forms(html):
    soup = BeautifulSoup(html, "html.parser")
    forms = []
    for f in soup.find_all("form"):
        has_password = bool(f.find("input", {"type":"password"}))
        action = f.get("action") or ""
        method = f.get("method") or "GET"
        if has_password or "login" in action.lower() or "signin" in action.lower():
            forms.append({"action": action, "method": method, "has_password": has_password})
    return forms

def run(host):
    url = host if host.startswith("http") else f"https://{host}"
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": DEFAULT_USER_AGENT})
    except Exception as e:
        LOG.debug("web request failed %s: %s", url, e)
        return {"error": str(e)}
    missing = _check_headers(resp)
    forms = _find_login_forms(resp.text)
    return {"status_code": resp.status_code, "missing_headers": missing, "forms": forms}
