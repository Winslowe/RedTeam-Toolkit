#!/usr/bin/env python3
"""
ZIP Password Cracker (Dictionary Attack)
========================================
"""
import zipfile
import sys

def crack_zip(zip_path, wordlist_path):
    try:
        with zipfile.ZipFile(zip_path) as zf:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                for word in f:
                    word = word.strip()
                    try:
                        zf.extractall(pwd=word.encode('utf-8'))
                        print(f"[!] Parola Kırıldı: {word}")
                        return
                    except:
                        pass
        print("[-] Parola sözlükte bulunamadı.")
    except Exception as e:
        print(f"[-] Hata: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanım: python Zip_Cracker.py <ZIP_DOSYASI> <WORDLIST>")
        sys.exit(1)
    crack_zip(sys.argv[1], sys.argv[2])
