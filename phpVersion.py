import requests

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

def check_php_version(domain):
    schemes = ['https://', 'http://']
    for scheme in schemes:
        try:
            url = domain if domain.startswith("http") else scheme + domain
            response = requests.get(url, timeout=5, allow_redirects=True)
            headers = response.headers

            print(f"[{response.status_code}] {url}")
            php_found = False

            for key, value in headers.items():
                line = f"{key}: {value}"
                if 'php' in key.lower() or 'php' in value.lower():
                    php_found = True
                    print(f"{RED}{line}{RESET}")
                else:
                    print(line)

            if php_found:
                print(f"{GREEN}[FOUND] PHP version detected in headers.{RESET}\n")
            else:
                print(f"[NO INFO] PHP version not found in headers.\n")

            return

        except requests.exceptions.RequestException:
            continue

    print(f"[ERROR] {domain} => Unable to connect via HTTP or HTTPS\n")

def main():
    try:
        with open("list.txt", "r") as file:
            domains = [line.strip() for line in file if line.strip()]

        for domain in domains:
            check_php_version(domain)

    except FileNotFoundError:
        print("❌ File 'list.txt' tidak ditemukan!")

if __name__ == "__main__":
    main()
