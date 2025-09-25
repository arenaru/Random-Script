import requests
import re

headers = {"User-Agent": "Mozilla/5.0"}

with open("list.txt") as file:
    domains = [
        line.strip().replace("https://", "").replace("http://", "").replace("/", "")
        for line in file if line.strip()
    ]

for domain in domains:
    print(f"\n🔍 Scanning: {domain}")
    try:
        r = requests.get(f"https://{domain}", headers=headers, timeout=10)
        js_files = re.findall(r'src=["\'](.*?\.js)["\']', r.text)

        for js_path in js_files:
            if not js_path.startswith("http"):
                js_url = f"https://{domain}/{js_path.lstrip('/')}"
            else:
                js_url = js_path

            try:
                res = requests.get(js_url, headers=headers, timeout=10)
                match = re.search(r'sourceMappingURL=([^\s]+)', res.text)
                if match:
                    map_path = match.group(1)
                    if map_path.startswith("http"):
                        map_url = map_path
                    else:
                        map_url = js_url.rsplit('/', 1)[0] + '/' + map_path

                    map_res = requests.get(map_url, headers=headers, timeout=10)
                    if map_res.status_code == 200:
                        print(f"  ⚠️ Found exposed source map: {map_url}")
            except Exception as e:
                print(f"  ⚠️ Error reading JS file: {js_url} - {e}")

    except Exception as e:
        print(f"  ❌ Cannot access {domain}: {e}")
