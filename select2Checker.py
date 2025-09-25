import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'
}

def cari_file_select2(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script', src=True)
    select2_links = [urljoin(base_url, s['src']) for s in scripts if 'select2' in s['src'].lower()]
    return select2_links

def ekstrak_versi_dari_js(js_url):
    try:
        r = requests.get(js_url, headers=headers, timeout=10)
        content = r.text

        # Dari isi file JS
        match = re.search(r'Select2\s+(\d+\.\d+\.\d+)', content)
        if match:
            return match.group(1)

        # Atau dari nama file
        match2 = re.search(r'select2.*?[@-](\d+\.\d+\.\d+)', js_url)
        if match2:
            return match2.group(1)
    except:
        pass
    return None

def cek_select2_version(target_url):
    try:
        print(f"[+] Mengakses {target_url}")
        r = requests.get(target_url, headers=headers, timeout=10)
        html = r.text

        js_links = cari_file_select2(html, target_url)

        if not js_links:
            print("[-] Tidak ditemukan file Select2.")
            return

        for js in js_links:
            print(f"    [*] Cek: {js}")
            versi = ekstrak_versi_dari_js(js)
            if versi:
                print(f"    [✓] Select2 versi: {versi}")
                if versi <= "4.0.5":
                    print("    [⚠️] Versi ini rentan terhadap XSS (CVE terkait AJAX remote data template).")
                else:
                    print("    [✅] Versi ini aman dari CVE XSS tersebut.")
                return

        print("[-] Tidak bisa mengekstrak versi dari file Select2.")
    
    except Exception as e:
        print(f"[!] Error: {e}")

# === MAIN ===
if __name__ == "__main__":
    target = input("Masukkan URL target (contoh: https://example.com): ")
    cek_select2_version(target)
