import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse

def sanitize(domain):
    domain = domain.strip()
    if domain.startswith("http://") or domain.startswith("https://"):
        domain = urlparse(domain).netloc
    return domain.split("/")[0]

def check_tls_ssl(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(5)
            s.connect((domain, 443))
            cert = s.getpeercert()
            protocol = s.version()

            print(f"\n🔍 Domain: {domain}")
            print(f"  ➤ TLS Version : {protocol}")
            print(f"  ➤ Valid From  : {cert['notBefore']}")
            print(f"  ➤ Valid Until : {cert['notAfter']}")

    except Exception as e:
        print(f"\n❌ Failed: {domain} - {e}")

# === MAIN ===
if __name__ == "__main__":
    try:
        with open("list.txt", "r") as f:
            domains = [sanitize(line) for line in f if line.strip()]
            for domain in domains:
                check_tls_ssl(domain)
    except FileNotFoundError:
        print("[!] File 'list.txt' tidak ditemukan.")
