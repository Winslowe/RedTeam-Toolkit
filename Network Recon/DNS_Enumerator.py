#!/usr/bin/env python3
"""
DNS Enumerator (Eğitim Amaçlı)
===============================
DNS kayıt tiplerini sorgular ve zone transfer dener.
"""
import socket
import sys

RECORD_TYPES = {
    "A": "IPv4 Adresi",
    "AAAA": "IPv6 Adresi",
    "MX": "Mail Sunucusu",
    "NS": "Name Server",
    "TXT": "TXT Kaydı",
    "CNAME": "Canonical Name",
}

def dns_lookup(domain):
    """Temel DNS sorgusu"""
    print(f"[*] DNS Sorgusu: {domain}")
    print("-" * 50)

    # A kaydı
    try:
        ips = socket.getaddrinfo(domain, None, socket.AF_INET)
        seen = set()
        for info in ips:
            ip = info[4][0]
            if ip not in seen:
                print(f"  [A]     {ip}")
                seen.add(ip)
    except socket.gaierror:
        print(f"  [-] A kaydı bulunamadı.")

    # AAAA kaydı
    try:
        ips6 = socket.getaddrinfo(domain, None, socket.AF_INET6)
        seen6 = set()
        for info in ips6:
            ip6 = info[4][0]
            if ip6 not in seen6:
                print(f"  [AAAA]  {ip6}")
                seen6.add(ip6)
    except socket.gaierror:
        pass

    # MX kaydı (basit DNS sorgusu)
    try:
        mx_records = socket.getaddrinfo(f"mail.{domain}", None)
        for info in mx_records[:2]:
            print(f"  [MX]    {info[4][0]}")
    except socket.gaierror:
        pass

    # Reverse DNS
    try:
        main_ip = socket.gethostbyname(domain)
        reverse = socket.gethostbyaddr(main_ip)
        print(f"  [PTR]   {reverse[0]}")
    except (socket.herror, socket.gaierror):
        pass

    print("-" * 50)

def subdomain_bruteforce(domain, wordlist_path):
    """Alt alan adı brute-force"""
    print(f"\n[*] Alt alan adı taraması: {domain}")
    found = []
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                sub = line.strip()
                if not sub:
                    continue
                target = f"{sub}.{domain}"
                try:
                    ip = socket.gethostbyname(target)
                    found.append((target, ip))
                    print(f"  [+] {target:<35} → {ip}")
                except socket.gaierror:
                    pass
    except FileNotFoundError:
        print(f"  [-] Wordlist bulunamadı: {wordlist_path}")

    print(f"\n[+] {len(found)} alt alan adı bulundu.")
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
