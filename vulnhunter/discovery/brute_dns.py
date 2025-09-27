import dns.resolver, logging
LOG = logging.getLogger("vulnhunter.discovery.brute_dns")

def brute_dns(domain, wordlist_path, resolver_timeout=3):
    found = set()
    resolver = dns.resolver.Resolver()
    resolver.timeout = resolver.lifetime = resolver_timeout
    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as fh:
            words = [w.strip() for w in fh if w.strip()]
    except Exception as e:
        LOG.error("wordlist open error: %s", e)
        return found

    for w in words:
        name = f"{w}.{domain}"
        try:
            answers = resolver.resolve(name, "A")
            if answers:
                found.add(name)
        except Exception:
            continue
    return found
