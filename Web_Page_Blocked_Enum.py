import requests
from requests.exceptions import RequestException, ConnectionError
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

for domain in domains:
    try:
        print(f"\n🔍 Checking {domain} ...")
        # disable auto redirect follow
        response = requests.get(domain, headers=headers, timeout=10, allow_redirects=False)
        
        # Check for redirect to HTTPS
        if response.status_code in [301, 302, 303, 307, 308]:
            location = response.headers.get('Location', '')
            if location.startswith("https://"):
                print(f"🔁 Redirected to HTTPS → Skipped: {domain}")
                continue

        # No redirect to HTTPS
        if response.status_code == 503 or "Web Page Blocked" in response.text:
            print(f"🚫 Blocked Content or 503: {domain}")
            with open("web_blocked.txt", "a") as f:
                f.write(domain + "\n")
        else:
            print(f"✅ HTTP {response.status_code}: {domain}")
    except ConnectionError as ce:
        msg = str(ce)
        if "Name or service not known" in msg or "Failed to resolve" in msg:
            print(f"❌ DNS Error: {domain}")
            with open("dns_error.txt", "a") as f:
                f.write(domain + "\n")
        else:
            print(f"⚠️ Connection Error: {domain} - {msg}")
            with open("connection_error.txt", "a") as f:
                f.write(domain + "\n")
        
    except RequestException as e:
        print(f"⚠️ Request Failed: {domain} - {e}")
    
    time.sleep(1)
