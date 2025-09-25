import requests
import re

GREEN = "\033[92m"
RESET = "\033[0m"

def check_csp(domain):
    if not domain.startswith("http"):
        domain = "https://" + domain

    try:
        response = requests.get(domain, timeout=5)
        csp = response.headers.get("Content-Security-Policy", "")

        print(f"[{response.status_code}] {domain}")

        if csp:
            # Cari directive default-src
            match = re.search(r'default-src[^;]*', csp)
            if match:
                highlighted = csp.replace(match.group(), f"{GREEN}{match.group()}{RESET}")
                print("✅ CSP found with default-src:")
                print(highlighted)
            else:
                print("⚠️ CSP found, but no default-src directive:")
                print(csp)
        else:
            print("❌ No Content-Security-Policy header found.")

        print()

    except Exception as e:
        print(f"[ERROR] {domain} => {e}\n")

def main():
    try:
        with open("list.txt", "r") as file:
            domains = [line.strip() for line in file if line.strip()]

        for domain in domains:
            check_csp(domain)

    except FileNotFoundError:
        print("❌ File 'list.txt' tidak ditemukan.")

if __name__ == "__main__":
    main()
