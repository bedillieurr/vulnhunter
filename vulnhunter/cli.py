import json
import os
import click
from .logger import get_logger
from .discovery import crtsh, brute_dns
from .scanners import webscan, nmap_wrapper
from .enrichment import simple_enricher
from .scoring import rules as scoring_rules
from .reporting.reporter import Reporter

LOG = get_logger()

@click.group()
@click.option("--verbose", is_flag=True, help="Enable verbose logging")
def cli(verbose):
    LOG.setLevel("DEBUG" if verbose else "INFO")

@cli.command()
@click.option("--domain", required=True, help="Target domain")
@click.option("--output", default=None, help="Save JSON results")
@click.option("--brute", is_flag=True, help="Enable DNS brute force")
@click.option("--wordlist", default="wordlists/common-subdomains.txt")
def subdomain(domain, output, brute, wordlist):
    """Passive subdomain enum (crt.sh); optionally brute-force DNS."""
    LOG.info("Enumerating subdomains for %s", domain)
    subs = set(crtsh.query_crtsh(domain))
    if brute:
        subs |= brute_dns.brute_dns(domain, wordlist)
    res = {"domain": domain, "subdomains": sorted(subs)}
    if output:
        os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
        with open(output, "w") as fh:
            json.dump(res, fh, indent=2)
        LOG.info("Saved results to %s", output)
    else:
        print(json.dumps(res, indent=2))

@cli.command()
@click.option("--target", required=True, help="Target (domain or IP)")
@click.option("--active", is_flag=True, help="Run active scans (nmap, webscan)")
@click.option("--output", default=None, help="Save JSON results")
@click.option("--html", default=None, help="Also save HTML report to this path")
def run(target, active, output, html):
    """End-to-end pipeline: discovery → enrichment → scoring → (optional active)."""
    LOG.info("Starting pipeline for %s (active=%s)", target, active)
    result = {"target": target, "findings": []}

    # discovery
    subs = set(crtsh.query_crtsh(target))
    result["discovery"] = {"subdomains": sorted(subs)}

    # enrichment
    enriched = simple_enricher.enrich_subdomains(list(subs))
    result["enrichment"] = enriched

    # scoring
    scored = scoring_rules.score_findings(enriched)
    result["scored"] = scored

    # optional active scans (top N only)
    if active and scored:
        LOG.info("Active scans enabled; running webscan & nmap on top 10")
        for item in scored[:10]:
            host = item["host"]
            item["active"] = {
                "web": webscan.run(host),
                "nmap": nmap_wrapper.run_scan(host, ports="80,443", fast=True),
            }

    # reporting
    if output:
        os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
        with open(output, "w") as fh:
            json.dump(result, fh, indent=2)
        LOG.info("Saved JSON pipeline results to %s", output)

    if html:
        Reporter(result).to_html(html)

    if not output and not html:
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    cli()
