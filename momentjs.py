import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_moment_js_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script', src=True)
    moment_links = [urljoin(base_url, s['src']) for s in scripts if 'moment' in s['src']]
    return moment_links

def extract_version_from_js(js_url):
    try:
        r = requests.get(js_url, timeout=10)
        match = re.search(r'version\s*[:=]\s*[\'"](\d+\.\d+\.\d+)[\'"]', r.text, re.IGNORECASE)
        if match:
            return match.group(1)
        # fallback: cari versi dari komentar awal
        match2 = re.search(r'moment\.js.*?(\d+\.\d+\.\d+)', r.text, re.IGNORECASE)
        if match2:
            return match2.group(1)
    except:
        pass
    return None

def check_moment_version_from_url(url):
    try:
        print(f"[+] Mengakses {url} ...")
        r = requests.get(url, timeout=10)
        moment_js_links = find_moment_js_links(r.text, url)

        if not moment_js_links:
            print("[-] Tidak ditemukan file moment.js pada halaman tersebut.")
            return

        for js_url in moment_js_links:
            print(f"    [*] Cek file: {js_url}")
            version = extract_version_from_js(js_url)
            if version:
                print(f"    [✓] Versi moment.js terdeteksi: {version}")
                return
        print("[-] Tidak dapat mengekstrak versi dari file moment.js.")
    except Exception as e:
        print(f"[!] Error: {e}")

# === MAIN ===
if __name__ == "__main__":
    target_url = input("Masukkan URL target (contoh: https://example.com): ")
    check_moment_version_from_url(target_url)
