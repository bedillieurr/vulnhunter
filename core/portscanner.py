import nmap

def scan_ports(target):
    nm = nmap.PortScanner()
    print(f"[*] Scanning {target} with Nmap...")
    nm.scan(target, arguments="-sS -T4")
    for host in nm.all_hosts():
        print(f"Host: {host} ({nm[host].hostname()})")
        print(f"State: {nm[host].state()}")
        for proto in nm[host].all_protocols():
            print(f"Protocol: {proto}")
            ports = nm[host][proto].keys()
            for port in sorted(ports):
                print(f"Port: {port}\tState: {nm[host][proto][port]['state']}")
