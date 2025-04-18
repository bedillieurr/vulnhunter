# 🔍 VulnHunt

**VulnHunt** is a modular, CLI-based red team toolkit for asset discovery and vulnerability enumeration.  
It helps you scan open ports and enumerate **active subdomains** using certificate transparency and DNS brute-force.

---

## 🚀 Features

- ✅ Port scanner (Nmap wrapper)
- ✅ Service detection (product/version)
- ✅ Subdomain enumeration from crt.sh
- ✅ DNS brute-force with wordlist
- ✅ Active subdomain filtering (live check)
- 🧰 Built in Python 3 — portable & extensible

---

## 📦 Requirements

- Python 3.7+
- `nmap` installed on the system
- Python packages (in `requirements.txt`)

Install them with:

```bash
sudo apt update
sudo apt install nmap python3-pip -y
pip install -r requirements.txt
-
sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

## Usage

- python main.py <mode> [options]

Modes:
- scan → Port scan
- subenum → Subdomain enumeration
  
## Examples
Port Scan Example: 
- python main.py scan scanme.nmap.org --ports 1-1000
- python main.py 192.168.1.1 --ports 20-1000

Subdomain Enumeration Example:
- python main.py subenum example.com

  ` Uses crt.sh and DNS brute-force (wordlists/subdomains.txt) to find live subdomains.`

## 🛡️ Disclaimer

This tool is intended for educational and authorized penetration testing only.
You are responsible for your actions.

## 🤝 Contribution
Feel free to fork and PR!
Ideas, issues, and feature requests are welcome. Let's build a badass red team toolkit together 🛠️

