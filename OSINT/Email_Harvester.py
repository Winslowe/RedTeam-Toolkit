#!/usr/bin/env python3
"""
OSINT Email Harvester
=====================
Hedef domain için açık kaynaklardan e-posta adreslerini toplar.
Gereksinim: pip install requests bs4
"""
import requests
from bs4 import BeautifulSoup
import re
import sys
import time

def google_search(query, num_pages=2):
    print(f"[*] '{query}' için Google'da aranıyor...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    results = []
    for page in range(num_pages):
        start = page * 10
        url = f"https://www.google.com/search?q={query}&start={start}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            results.append(res.text)
            time.sleep(2) # Google banından kaçınmak için
        except Exception as e:
            print(f"[-] Google arama hatası: {e}")
            
    return "".join(results)

def harvest_emails(domain):
    print(f"[*] {domain} için e-posta adresleri toplanıyor...\n")
    
    # Hedef domain formatına uygun email regex'i
    email_regex = r'[a-zA-Z0-9._%+-]+@' + re.escape(domain)
    
    emails = set()
    
    # 1. Arama Motoru Dorking (Google)
    query = f'"{domain}" email'
    html_content = google_search(query, 3)
    
    found_emails = re.findall(email_regex, html_content)
    for email in found_emails:
         emails.add(email.lower())
         
    # 2. Doğrudan site taraması (Ana sayfa ve iletişim)
    urls_to_check = [
        f"http://www.{domain}",
        f"https://www.{domain}",
        f"http://www.{domain}/contact",
        f"https://www.{domain}/iletisim",
        f"https://www.{domain}/about"
    ]
    
    print("\n[*] Web sitesi doğrudan taranıyor...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for url in urls_to_check:
        try:
            res = requests.get(url, headers=headers, timeout=5, verify=False)
            found = re.findall(email_regex, res.text)
            for email in found:
                emails.add(email.lower())
        except:
            pass

    # Sonuçları yazdır
    print("\n" + "="*50)
    if emails:
        print(f"[+] Toplam {len(emails)} e-posta adresi bulundu:\n")
        for email in sorted(emails):
            print(f"  -> {email}")
    else:
        print("[-] Hiç e-posta adresi bulunamadı.")
    print("="*50)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    if len(sys.argv) < 2:
        print("Kullanım: python Email_Harvester.py <hedef_domain>")
        print("Örnek: python Email_Harvester.py example.com")
        sys.exit(1)
        
    harvest_emails(sys.argv[1])
