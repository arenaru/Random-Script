import subprocess

with open("list.txt") as file:
	domains = [
		line.strip().replace("https://", "").replace("http://", "").replace("/", "")
		for line in file if line.strip()
	]

for domain in domains:
	try:
		result = subprocess.run(["nmap", "--script", "ssl-enum-ciphers", "-p", "443", domain], capture_output=True, text = True)
		print(f"\n🔎 {domain}")
		print(result.stdout)
	except Exception as e:
		print(f"!!ERROR!! {domain}: {e}")
