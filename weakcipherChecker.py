import subprocess
import re
from collections import defaultdict

def cek_weak_cipher(ip_or_domain):
    try:
        result = subprocess.run(
            ["nmap", "-p", "443", "--script", "ssl-enum-ciphers", ip_or_domain],
            capture_output=True, text=True
        )
        output = result.stdout

        weak_ciphers = defaultdict(list)
        current_version = None

        # Define cipher categories
        dangerous_keywords = ["RC4", "DES", "NULL", "MD5", "EXP", "aNULL", "LOW"]
        deprecated_keywords = ["CBC"]

        for line in output.splitlines():
            line = line.strip()

            # Identify TLS/SSL version block
            proto_match = re.match(r"^\|?\s*(TLSv?\d\.\d|SSLv3|SSL):?", line)
            if proto_match:
                current_version = proto_match.group(1)
                continue

            # Check for DANGEROUS ciphers
            if any(keyword in line for keyword in dangerous_keywords):
                key = f"{current_version or 'UNKNOWN'} [DANGEROUS]"
                weak_ciphers[key].append(line)

            # Check for DEPRECATED ciphers
            elif any(keyword in line for keyword in deprecated_keywords):
                key = f"{current_version or 'UNKNOWN'} [DEPRECATED]"
                weak_ciphers[key].append(line)

        return weak_ciphers

    except Exception as e:
        return f"⚠️ Error: {e}"

if __name__ == "__main__":
    try:
        with open("list.txt") as f:
            targets = [
                re.sub(r'^https?://', '', line.strip().rstrip('/')) 
                for line in f if line.strip()
            ]
    except FileNotFoundError:
        print("❌ File 'list.txt' not found.")
        exit()

    for target in targets:
        print(f"\n🔍 Scanning {target} for WEAK CIPHER SUITES...\n")
        result = cek_weak_cipher(target)

        if isinstance(result, str):
            print(result)
            continue

        if result:
            print("🚨 WEAK OR DEPRECATED CIPHER SUITES Detected!\n")
            for version, ciphers in result.items():
                print(f"🔐 {version}")
                for c in ciphers:
                    print(f"  - {c}")
                print()
        else:
            print("✅ No weak or deprecated cipher suites detected.")
