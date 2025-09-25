import ssl
import socket
from urllib.parse import urlparse

def sanitize(url):
    url = url.strip()
    if url.startswith("http://") or url.startswith("https://"):
        parsed = urlparse(url)
        return parsed.scheme, parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80)
    return "https", url, 443

def check_header(scheme, host, port):
    request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: curl/8.12.1\r\nAccept: */*\r\nConnection: close\r\n\r\n"

    try:
        sock = socket.create_connection((host, port), timeout=5)
        sock.settimeout(3)

        if scheme == "https":
            context = ssl._create_unverified_context()
            sock = context.wrap_socket(sock, server_hostname=host)

        sock.sendall(request.encode())
        response = b""
        while True:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
            except socket.timeout:
                break

        sock.close()
        decoded = response.decode(errors="ignore")
        headers = decoded.split("\r\n")

        print(f"\n🌐 {host}:{port} ({scheme.upper()})")
        print("──────────────────────────────────────────────────────────")
        for line in headers:
            print(line)
        print("──────────────────────────────────────────────────────────")

        found = False
        for h in headers:
            if "permission-policy" in h.lower():
                print("✅ Permission-Policy ditemukan")
                found = True
            elif "feature-policy" in h.lower():
                print("⚠️  Feature-Policy ditemukan (deprecated)")
                found = True
        if not found:
            print("❌ Tidak ditemukan header Permission-Policy atau Feature-Policy")

    except Exception as e:
        print(f"\n[!] Error koneksi ke {host}:{port} → {e}")

# === MAIN ===
if __name__ == "__main__":
    try:
        with open("list.txt", "r") as f:
            for line in f:
                if not line.strip():
                    continue
                scheme, host, port = sanitize(line)
                check_header(scheme, host, port)
    except FileNotFoundError:
        print("[!] File 'list.txt' tidak ditemukan.")
