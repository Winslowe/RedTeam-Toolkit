#!/usr/bin/env python3
"""
Directory Brute-Forcer (Eğitim Amaçlı)
=======================================
Web sunucularında gizli dizin ve dosya keşfi yapar.
requests kütüphanesi gerektirir (pip install requests)
"""
import sys
import time
try:
    import requests
    requests.packages.urllib3.disable_warnings()
except ImportError:
    print("[-] Lütfen 'requests' kütüphanesini yükleyin: pip install requests")
    sys.exit(1)

COMMON_EXTENSIONS = ['', '.php', '.html', '.txt', '.bak', '.old', '.zip', '.sql']

def bruteforce_dirs(base_url, wordlist_path, extensions=None, timeout=5):
    """Dizin ve dosya brute-force"""
    if extensions is None:
        extensions = ['']

    base_url = base_url.rstrip('/')
    print(f"[*] Hedef    : {base_url}")
    print(f"[*] Wordlist : {wordlist_path}")
    print(f"[*] Uzantılar: {', '.join(extensions) if extensions != [''] else 'Yok (sadece dizin)'}")
    print("-" * 65)
    print(f"{'Durum':<8} {'Boyut':<10} {'URL'}")
    print("-" * 65)

    found = []
    checked = 0

    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip()
                if not word or word.startswith('#'):
                    continue

                for ext in extensions:
                    path = f"{base_url}/{word}{ext}"
                    checked += 1

                    try:
                        r = requests.get(path, timeout=timeout, verify=False,
                                         allow_redirects=False)

                        if r.status_code in [200, 301, 302, 403]:
                            size = len(r.content)
                            status_str = str(r.status_code)
                            found.append({"url": path, "status": r.status_code, "size": size})
                            print(f"  {status_str:<8} {size:<10} {path}")

                    except requests.RequestException:
                        pass

                    if checked % 100 == 0:
                        print(f"  ... {checked} URL kontrol edildi ...", end="\r")

    except FileNotFoundError:
        print(f"[-] Wordlist bulunamadı: {wordlist_path}")
        return []

    print("-" * 65)
    print(f"[+] Tarama tamamlandı. {len(found)} sonuç / {checked} deneme")
    return found

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanım: python Directory_Bruteforcer.py <URL> <WORDLIST> [--ext]")
        print("Örnek  : python Directory_Bruteforcer.py http://target.com wordlist.txt")
        print("Uzantı : python Directory_Bruteforcer.py http://target.com wordlist.txt --ext")
        sys.exit(1)

    url = sys.argv[1]
    wl = sys.argv[2]
    ext = COMMON_EXTENSIONS if len(sys.argv) > 3 and sys.argv[3] == '--ext' else ['']

    bruteforce_dirs(url, wl, ext)
