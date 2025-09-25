import requests
from bs4 import BeautifulSoup

def check_js_versions(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script', src=True)
        for script in scripts:
            src = script['src']
            if 'jquery' in src.lower():
                print(f"{url} uses jQuery: {src}")
            elif 'bootstrap' in src.lower():
                print(f"{url} uses Bootstrap: {src}")
            # Tambahkan pengecekan untuk library lain sesuai kebutuhan
    except Exception as e:
        print(f"Error accessing {url}: {e}")

with open('list.txt', 'r') as file:
    urls = [line.strip() for line in file if line.strip()]
    for url in urls:
        check_js_versions(url)
