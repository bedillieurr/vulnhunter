import argparse
from core.portscanner import scan_target
from core.subdomain_enum import enumerate_active_subdomains


def print_results(results):
    print("\n[+] Scan Results:")
    for res in results:
        print(f"  - Port {res['port']} [{res['state']}]: {res['product']} {res['version']} ({res['name']})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VulnHunt - Port Scanner")
    parser.add_argument("target", help="IP address or domain to scan")
    parser.add_argument("--ports", help="Ports to scan (default: 1-1000)", default="1-1000")
    args = parser.parse_args()

    results = scan_target(args.target, args.ports)
    print_results(results)
