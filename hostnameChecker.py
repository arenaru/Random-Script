import ssl
import socket

# Baca daftar target dari list.txt
with open("list.txt") as f:
    targets = [line.strip() for line in f if line.strip()]

# Output file
ok_file = open("cert_match.txt", "w")
mismatch_file = open("cert_mismatch.txt", "w")
error_file = open("cert_error.txt", "w")

for target in targets:
    print(f"\n🔗 Target -> {target}")
    print("=======================================")
    try:
        hostname = target.replace("https://", "").replace("http://", "").split("/")[0]

        # Connect ke port 443
        ctx = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        # Ambil Common Name (CN)
        subject = dict(x[0] for x in cert["subject"])
        common_name = subject.get("commonName", "")

        # Ambil Subject Alternative Names (SAN)
        alt_names = []
        for typ, val in cert.get("subjectAltName", []):
            if typ == "DNS":
                alt_names.append(val)

        # Cocokkan hostname dengan CN atau SAN
        if hostname == common_name or hostname in alt_names:
            print(f"✅ MATCH: {hostname} valid for CN={common_name} SANs={alt_names}")
            ok_file.write(target + "\n")
        else:
            print(f"⚠️ MISMATCH: {hostname} not in CN={common_name} SANs={alt_names}")
            mismatch_file.write(f"{target} # CN={common_name} SANs={alt_names}\n")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        error_file.write(f"{target} # ERROR: {e}\n")

    print("=======================================")

# Close files
ok_file.close()
mismatch_file.close()
error_file.close()
