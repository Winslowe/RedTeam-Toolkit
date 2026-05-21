#!/usr/bin/env python3
"""
OSINT Whois Lookup
==================
Hedef domain için Whois bilgilerini sorgular.
Gereksinim: pip install python-whois
"""
import sys
try:
    import whois
except ImportError:
    print("[-] 'python-whois' kütüphanesi eksik. Kurulum: pip install python-whois")
    sys.exit(1)

def get_whois_info(domain):
    print(f"[*] Whois sorgusu yapılıyor: {domain}")
    print("-" * 50)
    
    try:
        w = whois.whois(domain)
        
        # Temel Bilgiler
        print(f"[+] Domain       : {w.domain_name}")
        print(f"[+] Registrar    : {w.registrar}")
        print(f"[+] Server       : {w.whois_server}")
        
        # Tarihler
        print("\n[*] Tarih Bilgileri:")
        if type(w.creation_date) == list:
            print(f"  -> Oluşturulma : {w.creation_date[0]}")
        else:
            print(f"  -> Oluşturulma : {w.creation_date}")
            
        if type(w.expiration_date) == list:
            print(f"  -> Bitiş       : {w.expiration_date[0]}")
        else:
            print(f"  -> Bitiş       : {w.expiration_date}")
            
        if type(w.updated_date) == list:
            print(f"  -> Güncellenme : {w.updated_date[0]}")
        else:
            print(f"  -> Güncellenme : {w.updated_date}")

        # Name Servers
        print("\n[*] Name Servers:")
        if w.name_servers:
            for ns in w.name_servers:
                print(f"  -> {ns}")
        else:
            print("  -> Bulunamadı")
            
        # Emails
        print("\n[*] İletişim E-Postaları:")
        if w.emails:
            if type(w.emails) == list:
                for email in set(w.emails):
                    print(f"  -> {email}")
            else:
                print(f"  -> {w.emails}")
        else:
            print("  -> Bulunamadı")
            
    except Exception as e:
        print(f"[-] Whois sorgusu başarısız: {e}")
    
    print("-" * 50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python Whois_Lookup.py <domain>")
        print("Örnek: python Whois_Lookup.py example.com")
        sys.exit(1)
        
    get_whois_info(sys.argv[1])
