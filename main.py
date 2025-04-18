import argparse
from core import (
    nmap_scanner, subdomain_enumeration, web_vuln_scanner,
    auth_bypass, web_crawler, ssl_http_security_audit,
    csp_checker, robots_txt_checker
)

def main():
    parser = argparse.ArgumentParser(description="VulnHunt - Red Team Tool Suite")
    subparsers = parser.add_subparsers(dest="command")

    # Nmap scanner
    nmap_parser = subparsers.add_parser("nmap")
    nmap_parser.add_argument("--target", required=True)

    # Subdomain enumeration
    subdomain_parser = subparsers.add_parser("subdomain")
    subdomain_parser.add_argument("--url", required=True)
    subdomain_parser.add_argument("--brute-force", action="store_true")

    # Web scan
    webscan_parser = subparsers.add_parser("webscan")
    webscan_parser.add_argument("--url", required=True)
    webscan_parser.add_argument("--input", help="Input file of subdomains")

    # Auth bypass
    auth_parser = subparsers.add_parser("auth_bypass")
    auth_parser.add_argument("--url", required=True)
    auth_parser.add_argument("--userlist", required=True)
    auth_parser.add_argument("--passlist", required=True)

    # Web crawler
    crawler_parser = subparsers.add_parser("crawl")
    crawler_parser.add_argument("--url", required=True)

    # SSL and headers audit
    ssl_parser = subparsers.add_parser("ssl_headers")
    ssl_parser.add_argument("--url", required=True)

    # CSP checker
    csp_parser = subparsers.add_parser("csp")
    csp_parser.add_argument("--url", required=True)

    # Robots.txt
    robots_parser = subparsers.add_parser("robots")
    robots_parser.add_argument("--url", required=True)

    args = parser.parse_args()

    if args.command == "nmap":
        nmap_scanner.scan_ports(args.target)
    elif args.command == "subdomain":
        subdomain_enumeration.enumerate(args.url, brute_force=args.brute_force)
    elif args.command == "webscan":
        web_vuln_scanner.scan(args.url, input_file=args.input)
    elif args.command == "auth_bypass":
        auth_bypass.run(args.url, args.userlist, args.passlist)
    elif args.command == "crawl":
        web_crawler.crawl(args.url)
    elif args.command == "ssl_headers":
        ssl_http_security_audit.audit(args.url)
    elif args.command == "csp":
        csp_checker.check(args.url)
    elif args.command == "robots":
        result = robots_txt_checker.check_robots_txt(args.url)
        print(result)

if __name__ == '__main__':
    main()
