import ssl
import socket
from datetime import datetime
from urllib.parse import urlparse
import pytz
import math

# Zona waktu WIB
wib = pytz.timezone('Asia/Jakarta')

# Warna ANSI
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RESET  = "\033[0m"

def sanitize(domain):
    domain = domain.strip()
    if domain.startswith("http://") or domain.startswith("https://"):
        domain = urlparse(domain).netloc
    return domain.split("/")[0]

def cek_ssl_expiry(domain, port=443, warning_days=60):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry_date_utc = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                expiry_date_wib = expiry_date_utc.replace(tzinfo=pytz.utc).astimezone(wib)
                now = datetime.now(pytz.utc).astimezone(wib)
                delta = expiry_date_wib - now

                total_seconds = delta.total_seconds()
                days_remaining = math.ceil(total_seconds / 86400)

                print(f"\n🔒 Domain        : {domain}")
                print(f"    ⏳ Expired pada : {expiry_date_wib.strftime('%a, %d %b %Y %H:%M:%S WIB')}")

                if days_remaining < 0:
                    expired_days = abs(days_remaining)
                    print(f"    🗓️  Status        : {RED}EXPIRED {expired_days} hari lalu{RESET}")
                elif days_remaining < warning_days:
                    print(f"    🗓️  Status        : {YELLOW}Akan expired dalam {days_remaining} hari{RESET}")
                else:
                    print(f"    🗓️  Status        : {GREEN}Masih aman ({days_remaining} hari lagi){RESET}")
    except Exception as e:
        print(f"\n[!] Gagal cek SSL untuk {domain} → {e}")

# === MAIN ===
if __name__ == "__main__":
    try:
        with open("list.txt", "r") as f:
            domains = [sanitize(line) for line in f if line.strip()]
            for domain in domains:
                cek_ssl_expiry(domain)
    except FileNotFoundError:
        print("[!] File 'list.txt' tidak ditemukan.")
