#!/bin/bash

# Script cek HSTS header
# Santahaus edition 😎

if [ $# -eq 0 ]; then
    echo "Usage: $0 <url1> <url2> ..."
    exit 1
fi

# UA Chrome Android biar server anggap sebagai browser
UA="Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36"

for url in "$@"; do
    echo "🔎 Checking $url ..."
    
    # ambil header response, follow redirect (-L), pakai UA browser
    response=$(curl -s -I -L -k -A "$UA" "$url")
    
    # cek HSTS
    hsts=$(echo "$response" | grep -i "strict-transport-security")
    
    if [ -n "$hsts" ]; then
        echo "✅ HSTS enabled: $hsts"
    else
        echo "❌ HSTS not found"
    fi
    echo
done
