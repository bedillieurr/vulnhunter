import requests, logging
from ..config import DEFAULT_USER_AGENT

LOG = logging.getLogger("vulnhunter.discovery.crtsh")

def query_crtsh(domain: str):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": DEFAULT_USER_AGENT})
        if r.status_code != 200:
            LOG.warning("crt.sh status %s", r.status_code)
            return set()
        data = r.json()
        subs = set()
        for entry in data:
            name = entry.get("name_value") or ""
            for n in name.splitlines():
                n = n.strip().lstrip("*.")
                if n.endswith(domain):
                    subs.add(n)
        return subs
    except Exception as e:
        LOG.exception("crt.sh error: %s", e)
        return set()
