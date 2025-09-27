# Architecture

```
vulnhunter/
  cli.py           # Click CLI entry
  logger.py        # unified logger
  config.py        # timeouts, UA, etc.
  discovery/       # crt.sh, brute DNS, future sources
  scanners/        # web headers/forms, nmap wrapper, future modules
  enrichment/      # combine discovery + scans into enriched entities
  scoring/         # simple additive rules → ranked findings
  reporting/       # JSON/HTML report + (later) baseline delta
  plugins/         # plugin loader (future)
```

**Pipeline (passive-first)**  
Discovery → Enrichment → Scoring → (optional Active) → Reporting.
