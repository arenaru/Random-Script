import subprocess
import re
import os

def cek_logjam(target):
    """
    Menjalankan nmap dengan senyap dan mengembalikan status dalam satu baris.
    """
    try:
        # Menjalankan nmap untuk mendapatkan output
        output = subprocess.check_output(
            ["nmap", "-p", "443", "--script", "ssl-enum-ciphers", target],
            text=True, stderr=subprocess.DEVNULL, timeout=300, encoding='utf-8', errors='ignore'
        )

        # Cukup cari kata kunci utamanya, gak perlu detail
        if "DHE_RSA" in output and re.search(r"\(dh\s*1024\)", output, re.IGNORECASE):
            return f"🔴 RENTAN   - {target}"
        elif "Host seems down" in output:
            return f"🟡 GAGAL    - {target} (Host mati atau port 443 ditutup)"
        else:
            return f"🟢 AMAN     - {target}"

    except FileNotFoundError:
        # Error ini fatal, jadi kita hentikan program
        return "STOP"
    except subprocess.TimeoutExpired:
        return f"❌ ERROR    - {target} (Timeout)"
    except Exception:
        return f"❌ ERROR    - {target} (Gagal dipindai)"

def main():
    target_file = "list.txt"

    if not os.path.exists(target_file):
        print(f"File '{target_file}' tidak ditemukan. Mohon buat filenya terlebih dahulu.")
        # Buat file contoh jika tidak ada
        with open(target_file, 'w') as f:
            f.write("# Masukkan domain/IP per baris\n")
            f.write("google.com\n")
        print(f"File contoh '{target_file}' telah dibuat.")
        return

    print("Memulai pemindaian Logjam...\n")
    
    with open(target_file, 'r') as f:
        targets = f.readlines()

    for line in targets:
        target = line.strip()
        if not target or target.startswith('#'):
            continue
        
        status = cek_logjam(target)
        
        if status == "STOP":
            print("❌ FATAL: 'nmap' tidak ditemukan. Pastikan nmap sudah terinstal.")
            break
        
        print(status)
    
    print("\n...Pemindaian selesai.")

if __name__ == "__main__":
    main()
