#!/usr/bin/env python3
"""
Advanced Hash Cracker
=====================
Supports MD5, SHA1, SHA256, NTLM with multiprocessing.
"""
import hashlib
import sys
import argparse
import concurrent.futures
import binascii

def hash_ntlm(password):
    return binascii.hexlify(hashlib.new('md4', password.encode('utf-16le')).digest()).decode()

ALGORITHMS = {
    'md5': lambda w: hashlib.md5(w.encode()).hexdigest(),
    'sha1': lambda w: hashlib.sha1(w.encode()).hexdigest(),
    'sha256': lambda w: hashlib.sha256(w.encode()).hexdigest(),
    'ntlm': hash_ntlm
}

def check_word(word, target_hash, algo_func):
    try:
        if algo_func(word) == target_hash:
            return word
    except Exception:
        pass
    return None

def crack_hash(target_hash, wordlist_path, algo_name):
    print(f"[*] Kırılmaya çalışılan hash: {target_hash}")
    print(f"[*] Algoritma: {algo_name.upper()}")
    
    algo_func = ALGORITHMS.get(algo_name.lower())
    if not algo_func:
        print(f"[-] Desteklenmeyen algoritma: {algo_name}")
        return

    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
             words = [line.strip() for line in f]
             
        print(f"[*] Wordlist yüklendi: {len(words)} kelime. Kırma işlemi başlıyor...")
        
        # Use ProcessPoolExecutor for CPU-bound hashing tasks
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Map words to futures, but process in chunks to avoid memory issues for huge lists
            # For simplicity in this script, we'll submit all. For production, consider generators.
            futures = [executor.submit(check_word, word, target_hash, algo_func) for word in words]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"\n[!] Parola Kırıldı: {result}")
                    # In a real app we'd cancel other futures, but simple exit is fine for script
                    return
        
        print("\n[-] Parola sözlükte bulunamadı.")
    except FileNotFoundError:
        print("[-] Wordlist dosyası bulunamadı.")
    except Exception as e:
        print(f"[-] Hata: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced Hash Cracker")
    parser.add_argument("-t", "--type", default="md5", choices=ALGORITHMS.keys(), help="Hash algoritması (varsayılan: md5)")
    parser.add_argument("hash", help="Kırılacak hash")
    parser.add_argument("wordlist", help="Wordlist dosyası yolu")
    
    args = parser.parse_args()
    crack_hash(args.hash, args.wordlist, args.type)
