#!/usr/bin/env python3
"""
CMS Vulnerability Scanner
=========================
WordPress, Joomla, Drupal gibi CMS'leri tespit eder ve versiyon analizi yapar.
Gereksinim: pip install requests beautifulsoup4
"""
import requests
import sys
import re

def detect_cms(url):
    print(f"[*] CMS Taraması Başlatıldı: {url}")
    print("-" * 50)
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        res = requests.get(url, headers=headers, timeout=10, verify=False)
        html = res.text.lower()
    except Exception as e:
        print(f"[-] Hedefe ulaşılamadı: {e}")
        return

    cms = "Bilinmiyor"
    version = "Bilinmiyor"

    # WordPress Tespiti
    if 'wp-content' in html or 'wp-includes' in html:
        cms = "WordPress"
        # Versiyon bulma (meta generator)
        match = re.search(r'<meta name="generator" content="wordpress (.*?)"', html)
        if match:
            version = match.group(1)
            
    # Joomla Tespiti
    elif 'joomla' in html or '/media/system/js/' in html:
        cms = "Joomla"
        match = re.search(r'<meta name="generator" content="joomla! - open source content management - version (.*?)"', html)
        if match:
            version = match.group(1)
            
    # Drupal Tespiti
    elif 'drupal' in html or 'sites/all/' in html:
        cms = "Drupal"
        match = re.search(r'<meta name="generator" content="drupal (.*?)"', html)
        if match:
            version = match.group(1)

    print(f"[+] Tespit Edilen CMS : \033[92m{cms}\033[0m")
    print(f"[+] Versiyon          : \033[93m{version}\033[0m")
    
    if cms != "Bilinmiyor" and version != "Bilinmiyor":
        print(f"\n[*] \033[96m{cms} {version}\033[0m için bilinen CVE'ler aranıyor...")
        # Örnek olarak public vulnerability db'ye sorgu atılabilir.
        # Basitlik için sadece WP için bilinen path'leri kontrol ediyoruz
        if cms == "WordPress":
            check_wp_files(url, headers)

    print("-" * 50)

def check_wp_files(url, headers):
    files_to_check = [
        "wp-config.php.bak",
        "wp-config.php~",
        "xmlrpc.php",
        "readme.html",
        "wp-admin/install.php"
    ]
    print("[*] Hassas dosyalar kontrol ediliyor...")
    for f in files_to_check:
        target = f"{url.rstrip('/')}/{f}"
        try:
            r = requests.head(target, headers=headers, timeout=5, verify=False)
            if r.status_code == 200:
                print(f"  \033[91m[!] BULUNDU:\033[0m {target}")
        except:
            pass

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    if len(sys.argv) < 2:
        print("Kullanım: python CMS_Scanner.py <URL>")
        sys.exit(1)
        
    url = sys.argv[1]
    if not url.startswith("http"):
        url = "http://" + url
        
    detect_cms(url)
