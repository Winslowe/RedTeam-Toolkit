#!/usr/bin/env python3
"""
Screenshot Grabber (Eğitim Amaçlı)
===================================
Hedef ekranını yakalar ve dosyaya kaydeder.
Pillow kütüphanesi gerektirir (pip install Pillow)
"""
import sys
import os
import time

try:
    from PIL import ImageGrab
except ImportError:
    print("[-] Lütfen 'Pillow' kütüphanesini yükleyin: pip install Pillow")
    sys.exit(1)

def take_screenshot(output_path="screenshot.png"):
    """Ekran görüntüsü al"""
    try:
        img = ImageGrab.grab()
        img.save(output_path)
        print(f"[+] Ekran görüntüsü kaydedildi: {os.path.abspath(output_path)}")
        return True
    except Exception as e:
        print(f"[-] Hata: {e}")
        return False

def continuous_capture(interval=10, count=5, output_dir="screenshots"):
    """Belirli aralıklarla sürekli ekran görüntüsü al"""
    os.makedirs(output_dir, exist_ok=True)
    print(f"[*] {count} ekran görüntüsü, {interval}sn aralıkla alınacak...")

    for i in range(count):
        ts = time.strftime("%Y%m%d_%H%M%S")
        path = os.path.join(output_dir, f"ss_{ts}.png")
        take_screenshot(path)
        if i < count - 1:
            time.sleep(interval)

    print(f"[+] Tamamlandı. Klasör: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        continuous_capture(interval, count)
    else:
        out = sys.argv[1] if len(sys.argv) > 1 else "screenshot.png"
        take_screenshot(out)
