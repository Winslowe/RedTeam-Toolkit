#!/usr/bin/env python3
"""
Basic Subdomain Enumerator
==========================
"""
import requests
import sys

def enum_subdomains(domain, wordlist_path):
    print(f"[*] Alt alan adları taranıyor: {domain}")
    try:
        with open(wordlist_path, 'r') as f:
            subdomains = f.read().splitlines()
            
        for sub in subdomains:
            url = f"http://{sub}.{domain}"
            try:
                requests.get(url, timeout=3)
                print(f"[+] Bulundu: {url}")
            except requests.ConnectionError:
                pass
    except FileNotFoundError:
        print("[-] Wordlist bulunamadı.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanım: python Subdomain_Enum.py <DOMAIN> <WORDLIST>")
        sys.exit(1)
    enum_subdomains(sys.argv[1], sys.argv[2])
