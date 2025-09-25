import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def extract_datatables_version_from_js(js_url):
    try:
        r = requests.get(js_url, timeout=10)
        # Cek di komentar awal file .js
        match = re.search(r'DataTables\s+([\d\.]+)', r.text)
        if match:
            return match.group(1)
    except:
        pass
    return None

def find_js_links_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script', src=True)
    js_links = [urljoin(base_url, script['src']) for script in scripts if 'dataTables' in script['src']]
    return js_links

def check_datatables_version(website_url):
    try:
        print(f'[+] Scanning: {website_url}')
        r = requests.get(website_url, timeout=10)
        js_links = find_js_links_from_html(r.text, website_url)

        if not js_links:
            print('[-] Tidak ditemukan link DataTables .js di halaman utama.')
            return

        for js_link in js_links:
            print(f'    [*] Menganalisis: {js_link}')
            version = extract_datatables_version_from_js(js_link)
            if version:
                print(f'    [✓] DataTables version: {version}')
                return
        print('[-] Tidak bisa mendeteksi versi dari file .js.')
    except Exception as e:
        print(f'[!] Error: {e}')

# Contoh pemakaian:
if __name__ == "__main__":
    target_url = input("Masukkan URL target (contoh: https://example.com): ")
    check_datatables_version(target_url)
