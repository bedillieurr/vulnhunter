import argparse
from core.portscanner import scan_target
from core.subdomain_enum import enumerate_active_subdomains


def print_results(results):
    print("\n[+] Scan Results:")
    for res in results:
        print(f"  - Port {res['port']} [{res['state']}]: {res['product']} {res['version']} ({res['name']})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VulnHunt - Modular Vulnerability Scanner")
    subparsers = parser.add_subparsers(dest="command")

    # Port scanner
    scan_parser = subparsers.add_parser("scan", help="Port scan mode")
    scan_parser.add_argument("target", help="IP/domain to scan")
    scan_parser.add_argument("--ports", help="Ports to scan", default="1-1000")

    # Subdomain enum
    sub_parser = subparsers.add_parser("subenum", help="Subdomain enumeration")
    sub_parser.add_argument("domain", help="Main domain (e.g., example.com)")

    args = parser.parse_args()

    if args.command == "scan":
        results = scan_target(args.target, args.ports)
        print_results(results)

    elif args.command == "subenum":
        subs = enumerate_active_subdomains(args.domain)
        print(f"\n[+] Active subdomains found ({len(subs)}):")
        for sub in subs:
            print(" -", sub)

    else:
        parser.print_help()
