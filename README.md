# 🔍 VulnHunter

**VulnHunter** is an open-source Red Team CLI tool designed for reconnaissance and vulnerability scanning of public-facing assets such as domains and IP addresses. This tool is made for ethical hackers, penetration testers, and security researchers who need efficient and automated security testing.

---

## 🚀 Features

- 🔍 **Port Scanner** (Nmap wrapper)
- 🌐 **Subdomain Enumeration** (crt.sh + DNS brute-force)
- 🕸️ **Web Vulnerability Scanner** (Login panel detection, redirects, HTTP headers, SSL info)
- 🔓 **Auth Bypass Tester** (Form brute-force with wordlists)
- 🧭 **Web Crawler** (Extract all links & forms)
- 📄 **robots.txt Analyzer**
- 🔐 **SSL & HTTP Security Header Audit**
- 🚫 **CORS & CSP Misconfiguration Check**

---

## 📦 Requirements

- Python 3.7+
- `nmap` installed on the system
- Python packages (in `requirements.txt`)

Install them with:

1. **Clone this repo:**
```bash
git clone https://github.com/bedillieurr/VulnHunt.git
```
```bash
cd vulnhunt
```

2. **Create a virtual environment (optional but recommended):**
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 🛠️ Usage

---
Run `main.py` with the desired module:

### 🔍 Nmap Scanner
```bash
python main.py nmap --target 192.168.1.1
```

### 🌐 Subdomain Enumeration
```bash
python main.py subdomain --url example.com
python main.py subdomain --url example.com --brute-force
```

### 🕸️ Web Vulnerability Scanner
```bash
python main.py webscan --url https://target.com
```

### 🔓 Auth Bypass (Login Brute-force)
```bash
python main.py auth_bypass --url https://target.com/login --userlist users.txt --passlist passwords.txt
```

### 🧭 Web Crawler
```bash
python main.py crawl --url https://target.com
```

### 📄 Robots.txt Checker
```bash
python main.py robots --url https://target.com
```

### 🔐 SSL & HTTP Header Audit
```bash
python main.py ssl_headers --url https://target.com
```

### ⚠️ CSP & CORS Check
```bash
python main.py csp --url https://target.com
```

---
  
## 📁 Sample Output

**Subdomain Enumeration:**
```
[*] Enumerating subdomains for example.com...
[+] Found subdomain: admin.example.com
[+] Found subdomain: dev.example.com
```

**Web Scan:**
```
[*] Scanning for web vulnerabilities on https://target.com
[!] Possible login/admin panel detected at https://target.com/login
[!] Missing header: X-Frame-Options
```

**Auth Bypass:**
```
[*] Trying admin:admin123
[*] Trying root:toor
[+] Possible valid credentials: root:toor
```

---

## ⚠️ Disclaimer

This tool is strictly intended for **ethical hacking** and **authorized security testing** only. Unauthorized use against systems you do not own or have permission to test is strictly prohibited.

---

## 🤝 Contribution
Feel free to fork and PR!
Ideas, issues, and feature requests are welcome. Let's build a badass red team toolkit together 🛠️

---

## 🔗 License

MIT License

---

Happy Hunting! 🐍
