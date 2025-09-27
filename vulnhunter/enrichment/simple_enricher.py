import logging
from ..scanners.webscan import run as web_run

LOG = logging.getLogger("vulnhunter.enrichment.simple_enricher")

def enrich_subdomains(subs):
    results = []
    for s in subs:
        web = web_run(s)
        tags = []
        if web.get("forms"):
            if any(f.get("has_password") for f in web["forms"]):
                tags.append("login_form")
        if web.get("missing_headers"):
            if web["missing_headers"]:
                tags.append("missing_security_headers")
        results.append({"host": s, "web": web, "tags": tags})
    return results
