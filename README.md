# 🔍 VulnHunt

**VulnHunt** is a modular CLI-based vulnerability scanning tool built for ethical hackers and red teamers. It helps you identify open ports and running services on public IPs/domains — the first step to knowing your attack surface.

---

## 🚀 Features

- ✅ TCP Port scanning
- ✅ Service detection (product & version)
- 📦 Output in human-readable format
- ⚙️ Built with Python and Nmap
- 🔒 Ethical hacking use only

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
```

##⚡ Usage
- python main.py <target> [--ports <port_range>]

## Examples:
- python main.py scanme.nmap.org
- python main.py 192.168.1.1 --ports 20-1000
