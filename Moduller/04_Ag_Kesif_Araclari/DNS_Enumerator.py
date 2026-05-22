#!/usr/bin/env python3
"""
Advanced DNS Enumerator
=======================
DNS kayıt tiplerini sorgular ve multi-threaded alt alan adı taraması yapar.
Gereksinim: pip install dnspython
"""
import socket
import sys
import concurrent.futures
try:
    import dns.resolver
except ImportError:
    print("[-] 'dnspython' modülü eksik. Yüklemek için: pip install dnspython")
    sys.exit(1)

def dns_lookup(domain):
    """Kapsamlı DNS sorgusu"""
    print(f"[*] DNS Sorgusu: {domain}")
    print("-" * 50)
    resolver = dns.resolver.Resolver()
    resolver.timeout = 2
    resolver.lifetime = 2

    records = {
        "A": "IPv4 Adresi",
        "AAAA": "IPv6 Adresi",
        "MX": "Mail Sunucusu",
        "NS": "Name Server",
        "TXT": "TXT Kaydı"
    }

    for record_type, desc in records.items():
        try:
            answers = resolver.resolve(domain, record_type)
            for rdata in answers:
                if record_type == "MX":
                    print(f"  [{record_type}] {desc:<15}: {rdata.exchange} (Pref: {rdata.preference})")
                else:
                    print(f"  [{record_type}] {desc:<15}: {rdata.to_text()}")
        except Exception:
            pass

    # Reverse DNS
    try:
        main_ip = socket.gethostbyname(domain)
        reverse = socket.gethostbyaddr(main_ip)
        print(f"  [PTR] Reverse DNS    : {reverse[0]}")
    except (socket.herror, socket.gaierror):
        pass

    print("-" * 50)

def check_subdomain(target):
    try:
        ip = socket.gethostbyname(target)
        return target, ip
    except socket.gaierror:
        return None, None

def subdomain_bruteforce(domain, wordlist_path):
    """Multi-threaded alt alan adı brute-force"""
    print(f"\n[*] Alt alan adı taraması: {domain}")
    found = []
    
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            subdomains = [line.strip() for line in f if line.strip()]
            
        print(f"[*] {len(subdomains)} kelime test ediliyor...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            targets = [f"{sub}.{domain}" for sub in subdomains]
            futures = {executor.submit(check_subdomain, target): target for target in targets}
            
            for future in concurrent.futures.as_completed(futures):
                target, ip = future.result()
                if target and ip:
                    found.append((target, ip))
                    print(f"  [+] {target:<35} → {ip}")
                    
    except FileNotFoundError:
        print(f"  [-] Wordlist bulunamadı: {wordlist_path}")

    print(f"\n[+] Toplam {len(found)} alt alan adı bulundu.")
    return found

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım:")
        print("  DNS Sorgusu  : python DNS_Enumerator.py example.com")
        print("  Subdomain BF : python DNS_Enumerator.py example.com wordlist.txt")
        sys.exit(1)

    domain = sys.argv[1]
    dns_lookup(domain)

    if len(sys.argv) >= 3:
        subdomain_bruteforce(domain, sys.argv[2])
