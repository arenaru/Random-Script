import ssl
import socket
from urllib.parse import urlparse
import time

def sanitize(url):
    url = url.strip()
    if url.startswith("http://") or url.startswith("https://"):
        parsed = urlparse(url)
        return parsed.scheme, parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80)
    return "https", url, 443

def check_trace(scheme, host, port):
    request = f"TRACE / HTTP/1.1\r\nHost: {host}\r\nUser-Agent: curl/8.12.1\r\nAccept: */*\r\n\r\n"

    try:
        sock = socket.create_connection((host, port), timeout=5)
        sock.settimeout(2)

        if scheme == "https":
            context = ssl._create_unverified_context()
            sock = context.wrap_socket(sock, server_hostname=host)

        sock.sendall(request.encode())

        response = b""
        start = time.time()
        while time.time() - start < 3:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
            except socket.timeout:
                break

        sock.close()

        decoded = response.decode(errors="ignore")
        print(f"\n🌐 {host}:{port} ({scheme.upper()})")
        print("──────────────────────────────────────────────────────────")
        print(decoded.strip())
        print("──────────────────────────────────────────────────────────")

        if "TRACE / HTTP" in decoded:
            print("❌ TRACE method ENABLED")
        else:
            print("✅ TRACE method DISABLED or blocked")

    except Exception as e:
        print(f"\n[!] Error connecting to {host}:{port} → {e}")

if __name__ == "__main__":
    try:
        with open("list.txt", "r") as f:
            for line in f:
                if not line.strip():
                    continue
                scheme, host, port = sanitize(line)
                check_trace(scheme, host, port)
    except FileNotFoundError:
        print("[!] File 'list.txt' tidak ditemukan.")
