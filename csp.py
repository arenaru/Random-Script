import requests
import urllib3
import socket

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def domain_resolves(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def cek_csp(url):
    try:
        response = requests.get(url, verify=False, timeout=5)
        csp = response.headers.get("Content-Security-Policy")

        print(f"\n🔍 Target -> {url}")
        print("📥 Response Headers:")
        for header, value in response.headers.items():
            print(f"  {header}: {value}")

        if csp:
            print("\n✅ CSP implemented.")
            print("📋 CSP Policy:", csp)
        else:
            print("\n❌ CSP Not Implemented.")

    except Exception as e:
        print(f"⚠️ Error accessing {url}: {e}")

if __name__ == "__main__":
    try:
        with open("list.txt") as f:
            targets = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("[!] File list.txt tidak ditemukan.")
        exit()

    for target in targets:
        if not target.startswith("http"):
            target = "https://" + target
        domain = target.split("//")[-1].split("/")[0]

        if domain_resolves(domain):
            cek_csp(target)
        else:
            print(f"\n❌ Cannot resolve domain: {domain} (SKIPPED)")
