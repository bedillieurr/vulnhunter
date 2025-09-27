import logging, subprocess
from shutil import which
try:
    import nmap
except Exception:
    nmap = None

LOG = logging.getLogger("vulnhunter.scanners.nmap")

def run_scan(target, ports="1-1024", fast=False):
    if which("nmap") is None:
        LOG.warning("nmap binary not found in PATH")
        return {"error": "nmap not installed"}
    if nmap:
        try:
            nm = nmap.PortScanner()
            args = "-sS -Pn" if fast else "-sV -sC -O -Pn"
            nm.scan(hosts=target, arguments=f"-p {ports} {args}")
            out = []
            for host in nm.all_hosts():
                for proto in nm[host].all_protocols():
                    for p in nm[host][proto].keys():
                        info = nm[host][proto][p]
                        out.append({"host": host, "port": p, "proto": proto, "state": info.get("state"), "service": info.get("name")})
            return {"result": out}
        except Exception as e:
            LOG.exception("python-nmap failed: %s", e)
    try:
        args = ["nmap", "-p", ports]
        args += ["-sS", "-Pn"] if fast else ["-sV", "-sC", "-O", "-Pn"]
        args.append(target)
        raw = subprocess.check_output(args, stderr=subprocess.STDOUT, universal_newlines=True, timeout=180)
        return {"raw": raw}
    except Exception as e:
        LOG.exception("nmap subprocess failed: %s", e)
        return {"error": str(e)}
