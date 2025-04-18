import requests

def check_robots_txt(url):
    if not url.endswith("/"):
        url += "/"
    robots_url = url + "robots.txt"
    try:
        r = requests.get(robots_url, timeout=5)
        if r.status_code == 200:
            lines = r.text.splitlines()
            risky = [l for l in lines if "Disallow:" in l and any(k in l.lower() for k in ["admin", "login", "config"])]
            if risky:
                return {"status": "warning", "risky_directives": risky}
            return {"status": "ok", "message": "robots.txt is clean."}
        return {"status": "error", "message": "robots.txt not found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
