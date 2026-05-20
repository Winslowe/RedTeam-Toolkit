#!/usr/bin/env python3
"""
Linux Privilege Escalation Checker (Basic)
==========================================
Checks for common misconfigurations that can lead to root access.
- SUID binaries
- Writable /etc/passwd
- Sudo privileges
"""
import os
import subprocess

def check_suid():
    print("[*] SUID Dosyaları Aranıyor...")
    try:
        output = subprocess.check_output("find / -perm -4000 -type f 2>/dev/null", shell=True).decode()
        for line in output.split("\n"):
            if line:
                print(f"  [+] SUID Bulundu: {line}")
    except:
        print("[-] SUID araması başarısız.")

def check_writable_passwd():
    print("\n[*] /etc/passwd Dosyası Yazılabilir mi?")
    if os.access("/etc/passwd", os.W_OK):
        print("  [!] UYARI: /etc/passwd dosyası yazılabilir! (Kritik zafiyet)")
    else:
        print("  [-] /etc/passwd yazılabilir değil.")

def check_sudo():
    print("\n[*] Sudo Yetkileri Kontrol Ediliyor (Parolasız)...")
    try:
        output = subprocess.check_output("sudo -l -n 2>/dev/null", shell=True).decode()
        print(output)
    except:
        print("  [-] Sudo parolasız kullanılamıyor veya yetki yok.")

if __name__ == "__main__":
    print("=== Linux Temel PrivEsc Kontrol Aracı ===\n")
    check_suid()
    check_writable_passwd()
    check_sudo()
    print("\n[+] Kontrol Tamamlandı.")
