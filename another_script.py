import requests
from requests.exceptions import RequestException, ConnectionError, ConnectTimeout
import time

# Load list domain dari file
with open("list.txt", "r") as f:
    raw_domains = [line.strip() for line in f if line.strip()]

# Force semua ke http://
domains = []
for d in raw_domains:
    if not d.startswith("http://"):
        domains.append("http://" + d)
    else:
        domains.append(d)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114 Safari/537.36'
}

def is_blocked(resp):
    return (
        resp.status_code == 503 or
        "Web Page Blocked" in resp.text or
        all(keyword in resp.text for keyword in ["User:", "URL:", "Category:"])
    )

for domain in domains:
    try:
        print(f"\n🔍 Checking {domain} ...")
        resp_http = requests.get(domain, headers=headers, timeout=10, allow_redirects=False)

        if is_blocked(resp_http):
            print(f"🚫 Blocked (HTTP): {domain}")
            with open("web_blocked_2.txt", "a") as f:
                f.write(domain + "\n")
            continue

        # Check redirect
        if resp_http.status_code in [301, 302, 303, 307, 308]:
            location = resp_http.headers.get('Location', '')
            if location.startswith("https://"):
                print(f"🔁 Redirecting to HTTPS: {location}")
                try:
                    resp_https = requests.get(location, headers=headers, timeout=10)
                    if is_blocked(resp_https):
                        print(f"🚫 Blocked (HTTPS): {domain}")
                        with open("web_blocked_2.txt", "a") as f:
                            f.write(domain + "\n")
                    else:
                        print(f"✅ OK after redirect: {domain}")
                except (ConnectionError, ConnectTimeout) as e:
                    print(f"❌ HTTPS Timeout/ConnectionError: {domain}")
                    with open("connection_error.txt", "a") as f:
                        f.write(domain + "\n")
            else:
                print(f"⚠️ Redirected to non-HTTPS: {location} → Skipped: {domain}")
        else:
            print(f"✅ OK (no redirect): {domain}")

    except ConnectionError as ce:
        msg = str(ce)
        if "Name or service not known" in msg or "Failed to resolve" in msg:
            print(f"❌ DNS Error: {domain}")
            with open("dns_error_2.txt", "a") as f:
                f.write(domain + "\n")
        else:
            print(f"⚠️ Connection Error: {domain} - {msg}")
            with open("connection_error_2.txt", "a") as f:
                f.write(domain + "\n")

    except RequestException as e:
        print(f"⚠️ Request Failed: {domain} - {e}")

    time.sleep(1)
