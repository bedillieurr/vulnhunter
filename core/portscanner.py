import nmap

def scan_target(target, ports="1-1000"):
    nm = nmap.PortScanner()
    print(f"[+] Scanning {target} on ports {ports} ...")
    nm.scan(hosts=target, arguments=f"-p {ports} -sV")

    results = []
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in sorted(lport):
                service = nm[host][proto][port]
                results.append({
                    "port": port,
                    "state": service["state"],
                    "name": service["name"],
                    "product": service.get("product", ""),
                    "version": service.get("version", "")
                })
    return results
