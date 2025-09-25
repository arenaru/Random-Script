import requests

# Domain yang mau dicek
url = "https://www.trans-cosmos.co.id"

# Kirim request HEAD untuk ambil header saja
response = requests.get(url)
csp = response.headers.get("Content-Security-Policy")

if not csp:
    print(f"❌ Tidak ada header CSP ditemukan di {url}")
else:
    print(f"✅ CSP ditemukan:\n{csp}\n")

    # Daftar direktif yang dianggap berbahaya
    unsafe_keywords = [
        "'unsafe-inline'", "'unsafe-eval'", "*", "data:", "blob:"
    ]

    # Cek dan laporkan yang digunakan
    print("🚨 Direktif Berisiko yang Ditemukan:")
    found_any = False
    for keyword in unsafe_keywords:
        if keyword in csp:
            print(f"❗ Mengandung: {keyword}")
            found_any = True

    if not found_any:
        print("✅ Tidak ditemukan direktif berisiko.")
