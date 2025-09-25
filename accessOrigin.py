import requests

RED = "\033[91m"
RESET = "\033[0m"

def check_cors(domain):
    if not domain.startswith("http"):
        domain = "https://" + domain

    try:
        headers = {
            "Origin": "https://evil.com",
            "Access-Control-Request-Method": "GET"
        }

        response = requests.options(domain, headers=headers, timeout=5)
        print(f"[{response.status_code}] {domain}")

        for key, value in response.headers.items():
            if key.lower() == "access-control-allow-origin" and "*" in value:
                print(f"{RED}{key}: {value}{RESET}")
            else:
                print(f"{key}: {value}")

        if "Access-Control-Allow-Origin" not in response.headers:
            print("⚪ No Access-Control-Allow-Origin header returned")

        print()

    except Exception as e:
        print(f"[ERROR] {domain} => {e}\n")

def main():
    try:
        with open("list.txt", "r") as file:
            targets = [line.strip() for line in file if line.strip()]

        for target in targets:
            check_cors(target)

    except FileNotFoundError:
        print("❌ File 'list.txt' tidak ditemukan.")

if __name__ == "__main__":
    main()
