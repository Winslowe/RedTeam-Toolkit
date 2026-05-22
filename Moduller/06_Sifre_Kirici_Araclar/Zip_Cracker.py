#!/usr/bin/env python3
"""
Advanced ZIP Password Cracker
=============================
Bellek üzerinden dictionary attack yapar (diske dosya çıkarmaz).
"""
import zipfile
import sys
import concurrent.futures

def attempt_extract(zip_path, word):
    try:
        with zipfile.ZipFile(zip_path) as zf:
            # Sadece dosyanın ilk öğesini bellekten okumayı dene (şifre doğrulama)
            first_file = zf.namelist()[0]
            zf.read(first_file, pwd=word.encode('utf-8'))
            return True
    except (RuntimeError, zipfile.BadZipFile):
        # Şifre yanlış
        return False
    except Exception:
        return False

def crack_zip(zip_path, wordlist_path):
    print(f"[*] ZIP Kırıcı başlatıldı. Dosya: {zip_path}")
    
    if not zipfile.is_zipfile(zip_path):
        print("[-] Geçersiz ZIP dosyası.")
        return

    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            words = [line.strip() for line in f if line.strip()]
            
        print(f"[*] Wordlist yüklendi ({len(words)} kelime). Kırılıyor...\n")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(attempt_extract, zip_path, word): word for word in words}
            
            for future in concurrent.futures.as_completed(futures):
                word = futures[future]
                if future.result():
                    print(f"[!] BAŞARILI! Parola Kırıldı: {word}")
                    return
                    
        print("[-] Parola sözlükte bulunamadı.")
    except FileNotFoundError:
        print("[-] Wordlist dosyası bulunamadı.")
    except Exception as e:
        print(f"[-] Hata: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanım: python Zip_Cracker.py <ZIP_DOSYASI> <WORDLIST>")
        sys.exit(1)
    crack_zip(sys.argv[1], sys.argv[2])
