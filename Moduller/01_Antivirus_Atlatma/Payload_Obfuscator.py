#!/usr/bin/env python3
"""
Python Payload Obfuscator
=========================
Python kodunu base64 ve exec() kullanarak gizler.
"""
import base64
import sys

def obfuscate_file(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            payload = f.read()
            
        b64_payload = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
        
        obfuscated_code = f"import base64\nexec(base64.b64decode('{b64_payload}').decode('utf-8'))"
        
        with open(output_file, 'w') as f:
            f.write(obfuscated_code)
            
        print(f"[+] Obfuscate işlemi başarılı. Yeni dosya: {output_file}")
    except Exception as e:
        print(f"[-] Hata: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanım: python Payload_Obfuscator.py <GIRIS_DOSYASI> <CIKIS_DOSYASI>")
        sys.exit(1)
    obfuscate_file(sys.argv[1], sys.argv[2])
