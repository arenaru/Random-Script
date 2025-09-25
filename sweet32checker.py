import subprocess
from urllib.parse import urlparse
import re

def load_targets(filename="list.txt"):
    targets = []
    with open(filename, "r") as f:
        for line in f:
            raw = line.strip()
            if not raw:
                continue
            parsed = urlparse(raw if raw.startswith("http") else f"https://{raw}")
            if parsed.hostname:
                targets.append(parsed.hostname)
    return targets

def extract_3des_per_protocol(output: str):
    results = {}
    current_proto = None
    cipher_pattern = re.compile(r'^TLS_.*3DES.*', re.IGNORECASE)

    for line in output.splitlines():
        line = line.strip().lstrip("|").strip()  # STRIP | dan spasi

        # detect start of protocol section (e.g. TLSv1.2:)
        proto_match = re.match(r'^([A-Z]+v?\d(\.\d+)?):$', line)
        if proto_match:
            current_proto = proto_match.group(1)
            results[current_proto] = []
            continue

        # match 3DES ciphers under the current protocol
        if current_proto and cipher_pattern.match(line):
            results[current_proto].append(line)

    return {k: v for k, v in results.items() if v}

def scan_target(target):
    try:
        result = subprocess.run(
            ["nmap", "--script", "ssl-enum-ciphers", "-p", "443", target],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            text=True
        )

        output = result.stdout
        proto_ciphers = extract_3des_per_protocol(output)

        if proto_ciphers:
            print(f"[⚠️ VULNERABLE] {target} - SWEET32 Detected")
            for proto, ciphers in proto_ciphers.items():
                print(f"  🔐 {proto}")
                for cipher in ciphers:
                    print(f"    ➤ {cipher}")
        elif "ssl-enum-ciphers:" in output:
            print(f"[✅ SAFE] {target} - No 3DES cipher detected")
        else:
            print(f"[❓ UNKNOWN] {target} - No SSL info found")

    except subprocess.TimeoutExpired:
        print(f"[⏰ TIMEOUT] {target} - Scan took too long")
    except Exception as e:
        print(f"[❌ ERROR] {target} - {e}")

def main():
    targets = load_targets()
    print("🚀 Starting SWEET32 scan...\n")
    for target in targets:
        scan_target(target)
        print()

if __name__ == "__main__":
    main()
