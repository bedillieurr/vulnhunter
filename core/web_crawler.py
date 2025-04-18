import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl(url):
    print(f"[*] Crawling: {url}")
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        links = set()
        for link in soup.find_all("a"):
            href = link.get("href")
            if href:
                links.add(urljoin(url, href))

        for link in sorted(links):
            print(f"[+] Link: {link}")

    except Exception as e:
        print(f"[x] Crawl failed: {e}")
