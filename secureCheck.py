import subprocess

# Load list of targets
with open("list.txt") as f:
    targets = [line.strip() for line in f if line.strip()]

# Output files
cookie_secure_file = open("cookie_secure.txt", "w")
cookie_insecure_file = open("cookie_insecure.txt", "w")
no_cookie_file = open("no_cookie.txt", "w")

# User-Agent (optional)
user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"

for target in targets:
    print(f"\n🌐 Target -> {target}")
    print("=======================================")
    try:
        # Use curl with -v to capture headers + final URL
        result = subprocess.run(
            [
                "curl", "-s", "-k", "-L",
                "-A", user_agent,
                "-D", "-",  # Dump headers
                "-w", "\n➡️ Final URL: %{url_effective}\n",
                "-o", "-",  # Output ke stdout
                target
            ],
            capture_output=True,
            text=True,
            timeout=5
        )

        headers = result.stdout
        final_url = ""
        for line in headers.splitlines():
            if line.startswith("➡️ Final URL:"):
                final_url = line.split("➡️ Final URL:")[1].strip()

        headers_lower = headers.lower()

        if "set-cookie:" in headers_lower:
            cookies = [line for line in headers.splitlines() if line.lower().startswith("set-cookie:")]
            has_secure = any("secure" in cookie.lower() for cookie in cookies)

            for cookie in cookies:
                print("🍪", cookie.strip())

            if has_secure:
                print("✅ Cookie is SECURE")
                cookie_secure_file.write(final_url + "\n")
            else:
                print("⚠️ Cookie is INSECURE (missing 'Secure')")
                cookie_insecure_file.write(final_url + "\n")
        else:
            print("🚫 No Set-Cookie header")
            no_cookie_file.write(final_url + "\n")

    except Exception as e:
        print(f"❌ Error: {e}")
        no_cookie_file.write(f"{target} # ERROR: {e}\n")

    print("=======================================")

# Close files
cookie_secure_file.close()
cookie_insecure_file.close()
no_cookie_file.close()
