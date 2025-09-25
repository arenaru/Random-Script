import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def cek_cookie_httponly(url):
    try:
        response = requests.get(url, verify=False, timeout=5)
        cookies = response.headers.getlist("Set-Cookie") if hasattr(response.headers, 'getlist') else response.headers.get("Set-Cookie", "").split(", ")

        print(f"\n🔍 Target -> {url}")
        if not cookies or cookies == [""]:
            print("❌ Tidak ditemukan header Set-Cookie.")
            return

        for cookie in cookies:
            parts = cookie.lower().split(";")
            name = parts[0].strip()
            if "httponly" not in parts:
                print(f"⚠️  Cookie tanpa HttpOnly: {name}")
            else:
                print(f"✅ Cookie aman (HttpOnly): {name}")

    except Exception as e:
        print(f"⚠️  Error akses {url}: {e}")

if __name__ == "__main__":
    try:
        with open("list.txt", "r") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("[!] File list.txt tidak ditemukan.")
        exit()

    for url in urls:
        if not url.startswith("http"):
            url = "https://" + url
        cek_cookie_httponly(url)
