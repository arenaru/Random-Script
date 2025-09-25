import requests

def cek_laravel_debug(url):
    # Pakai URL ngasal yang pasti error
    if not url.endswith('/'):
        url += '/'
    test_url = url + "__debugcheck123"

    print(f"[+] Mengakses: {test_url}")
    
    try:
        r = requests.get(test_url, timeout=10)

        indikasi = [
            "Whoops!",
            "Exception trace",
            "Stack trace",
            "Laravel",
            "vendor/laravel/framework",
            "APP_DEBUG"
        ]

        debug_detected = any(i.lower() in r.text.lower() for i in indikasi)

        if debug_detected:
            print("🚨 Laravel Debug Mode TERDETEKSI AKTIF! (APP_DEBUG=true)")
        else:
            print("✅ Laravel Debug Mode TIDAK terdeteksi (mungkin APP_DEBUG=false)")
        
        print(f"[i] Status code: {r.status_code}")
    
    except Exception as e:
        print(f"[!] Gagal mengakses: {e}")

# === MAIN ===
if __name__ == "__main__":
    target = input("Masukkan URL target (contoh: https://example.com): ")
    cek_laravel_debug(target)
