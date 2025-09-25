import subprocess

# Load target list
with open("list.txt") as f:
    targets = [line.strip() for line in f if line.strip()]

# User-Agent: Android Nexus 5
user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"

# Prepare output files
with_hsts_file = open("with_hsts.txt", "w")
without_hsts_file = open("without_hsts.txt", "w")
cant_be_reach_file = open("cant_be_reach.txt", "w")

# Loop through targets
for target in targets:
    # Tambah https:// kalau belum ada
    if not target.startswith("http://") and not target.startswith("https://"):
        target_url = "https://" + target
    else:
        target_url = target

    print(f"\n🔗 Target -> {target_url}")
    print("=======================================")
    try:
        result = subprocess.run(
            [
                "curl", "-I", "-k",
                "-A", user_agent,
                "-w", "\n➡️ Final URL: %{url_effective}\n📶 Status Code: %{http_code}\n",
                target_url
            ],
            capture_output=True,
            text=True,
            timeout=8
        )

        output = result.stdout.strip()
        stderr = result.stderr.strip()
        print(output)

        # Extract final URL
        final_url = ""
        for line in output.splitlines():
            if line.startswith("➡️ Final URL:"):
                final_url = line.split("➡️ Final URL:")[1].strip()

        # Extract status code
        if "📶 Status Code:" in output:
            status_line = output.split("📶 Status Code:")[-1].strip()
        else:
            status_line = "000"

        # Cek koneksi gagal
        if status_line == "000" or "could not resolve" in stderr.lower() or "connection refused" in stderr.lower():
            print("❌ Cannot be reached")
            cant_be_reach_file.write(f"{target_url}\n")

        # Cek HSTS di response
        elif "strict-transport-security:" in output.lower():
            print("🔐 HSTS: ✅ YES")
            with_hsts_file.write(final_url + "\n")
        else:
            print("🔓 HSTS: ❌ NO")
            without_hsts_file.write(final_url + "\n")

    except Exception as e:
        print(f"⚠️ Error: {e}")
        cant_be_reach_file.write(f"{target_url}\n")

    print("=======================================\n")

# Close files
with_hsts_file.close()
without_hsts_file.close()
cant_be_reach_file.close()
