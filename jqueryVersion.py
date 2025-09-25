import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_jquery_ui_scripts(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script', src=True)
    return [urljoin(base_url, s['src']) for s in scripts if 'jquery-ui' in s['src'].lower()]

def extract_ui_version(js_url):
    try:
        r = requests.get(js_url, timeout=10)
        content = r.text
        match = re.search(r'jQuery UI.*?v?(\d+\.\d+\.\d+)', content, re.IGNORECASE)
        if match:
            return match.group(1)
        match2 = re.search(r'jquery-ui[-\.]?(\d+\.\d+\.\d+)', js_url)
        if match2:
            return match2.group(1)
    except:
        pass
    return None

def scan_for_modules(html):
    modules = {
        "dialog": False,
        "datepicker": False,
        "tooltip": False,
        "tabs": False,
        "draggable": False,
        "sortable": False
    }
    combined = html.lower()
    for key in modules:
        if key in combined:
            modules[key] = True
    return modules

def cek_jquery_ui_dan_modul(domain_url):
    try:
        print(f"[+] Mengakses {domain_url} ...")
        r = requests.get(domain_url, timeout=10)
        html = r.text

        js_links = find_jquery_ui_scripts(html, domain_url)
        jquery_ui_version = None

        if not js_links:
            print("[-] Tidak ditemukan file jQuery UI.")
        else:
            for js_url in js_links:
                print(f"    [*] Cek file: {js_url}")
                version = extract_ui_version(js_url)
                if version:
                    jquery_ui_version = version
                    print(f"    [✓] Versi jQuery UI: {version}")
                    break
            else:
                print("[-] Versi jQuery UI tidak bisa dideteksi.")

        print("\n[+] Deteksi fitur jQuery UI:")
        modules = scan_for_modules(html)
        for mod, used in modules.items():
            if used:
                info = f"(HTML/JS, v{jquery_ui_version or '?'})"
            else:
                info = "(–)"
            print(f"    [✓] {mod:<12}: {'Aktif' if used else 'Tidak terdeteksi'} {info}")

    except Exception as e:
        print(f"[!] Error: {e}")

# === MAIN ===
if __name__ == "__main__":
    target = input("Masukkan URL target (contoh: https://example.com): ")
    cek_jquery_ui_dan_modul(target)
