#!/usr/bin/env python3
"""
Basic MD5 Hash Cracker (Dictionary Attack)
==========================================
"""
import hashlib
import sys

def crack_md5(target_hash, wordlist_path):
    print(f"[*] Kırılmaya çalışılan hash: {target_hash}")
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for word in f:
                word = word.strip()
                hashed_word = hashlib.md5(word.encode()).hexdigest()
                if hashed_word == target_hash:
                    print(f"[!] Parola Kırıldı: {word}")
                    return
        print("[-] Parola sözlükte bulunamadı.")
    except FileNotFoundError:
        print("[-] Wordlist dosyası bulunamadı.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanım: python Hash_Cracker.py <MD5_HASH> <WORDLIST>")
        sys.exit(1)
    crack_md5(sys.argv[1], sys.argv[2])
