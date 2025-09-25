import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Daftar regex versi dari konten JS
known_libraries = {
    "jquery": r"jQuery(?: JavaScript Library)? v?(\d+\.\d+(\.\d+)?)",
    "bootstrap": r"Bootstrap(?: v)?(\d+\.\d+(\.\d+)?)",
    "moment": r"Moment(?:\.js)? v?(\d+\.\d+(\.\d+)?)",
    "lodash": r"Lodash(?:\.js)? v?(\d+\.\d+(\.\d+)?)",
    "handlebars": r"Handlebars(?:\.js)? v?(\d+\.\d+(\.\d+)?)",
    "jquery ui": r"jQuery UI(?: -)? v?(\d+\.\d+(\.\d+)?)"
}

# Ekstrak dari URL CDN (misal: .../jquery/1.9.0/jquery.min.js)
def extract_from_url(js_url):
    for lib in known_libraries:
        pattern = rf"{lib}[\/\-\.]?(\d+\.\d+(\.\d+)?)[\/\-\.]"
        match = re.search(pattern, js_url, re.IGNORECASE)
        if match:
            return lib.title(), match.group(1)
    return None, None

# Ekstrak dari isi file JS
def extract_from_content(js_url):
    try:
        res = requests.get(js_url, timeout=5)
        content = res.text[:3000]  # cukup baca awal
        for lib, pattern in known_libraries.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return lib.title(), match.group(1)
    except:
        return None, None
    return None, None

def get_js_links(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        scripts = soup.find_all("script", src=True)
        return [urljoin(url, tag['src']) for tag in scripts]
    except:
        return []

def scan_site(domain):
    print(f"\n🔍 {domain.strip('/')}/")
    detected = set()
    js_files = get_js_links(domain)

    for js in js_files:
        lib, ver = extract_from_url(js)
        if not ver:
            lib, ver = extract_from_content(js)

        if lib and ver:
            entry = f"{lib} {ver}"
            if entry not in detected:
                print(f"    • {entry}")
                detected.add(entry)

    if not detected:
        print("    • (Tidak ada versi library dikenali)")

# === MAIN ===
if __name__ == "__main__":
    try:
        with open("list.txt", "r") as f:
            targets = [line.strip() for line in f if line.strip()]
            for url in targets:
                scan_site(url)
    except FileNotFoundError:
        print("[!] File 'list.txt' tidak ditemukan.")
