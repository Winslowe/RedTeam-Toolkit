#!/usr/bin/env python3
"""
Web Dashboard for The Ultimate Pentest Arsenal
==============================================
Flask tabanlı modern bir web arayüzü sunar.
Gereksinim: pip install flask
"""
import os
import sys
import subprocess
import threading
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))

def run_script(script_path, args):
    cmd = [sys.executable, script_path] + args
    try:
        # Aracı çalıştır ve çıktısını yakala
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return result.stdout + "\n" + result.stderr
    except subprocess.TimeoutExpired:
        return "[!] İşlem 120 saniyeyi aştığı için sonlandırıldı."
    except Exception as e:
        return f"[!] Hata: {e}"

@app.route('/')
def index():
    return render_template('index.html', output=None)

@app.route('/run/autopwn', methods=['POST'])
def run_autopwn():
    target = request.form.get('target', '').strip()
    if not target:
        return render_template('index.html', output="Hata: Hedef IP belirtilmedi.")
    
    script_path = os.path.join(base_dir, "Auto_Pwn.py")
    output = f"[*] Auto-Pwn başlatılıyor: {target}...\n"
    output += run_script(script_path, [target])
    return render_template('index.html', output=output)

@app.route('/run/phishing', methods=['POST'])
def run_phishing():
    port = request.form.get('port', '8080').strip()
    script_path = os.path.join(base_dir, "Social Engineering", "Phishing_Server.py")
    
    # Phishing Server'ı arka planda başlat
    cmd = [sys.executable, script_path, port, "https://google.com", "Oltalama Portalı"]
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    output = f"[*] Phishing Server başarıyla arka planda başlatıldı!\n[+] Port: {port}\n[+] Hedef URL: http://localhost:{port}/"
    return render_template('index.html', output=output)

@app.route('/run/cms_scanner', methods=['POST'])
def run_cms_scanner():
    url = request.form.get('url', '').strip()
    if not url:
        return render_template('index.html', output="Hata: Hedef URL belirtilmedi.")
    
    script_path = os.path.join(base_dir, "Web Exploitation", "CMS_Scanner.py")
    output = f"[*] CMS Taraması başlatılıyor: {url}...\n"
    output += run_script(script_path, [url])
    return render_template('index.html', output=output)

def start_web_server(port=5000):
    print(f"\n\033[92m[*] Web Dashboard Başlatılıyor...\033[0m")
    print(f"\033[96m[+] Lütfen tarayıcınızdan şu adrese gidin:\033[0m \033[4mhttp://127.0.0.1:{port}/\033[0m")
    print(f"\033[90m(Web arayüzünü kapatmak için terminalde CTRL+C yapın)\033[0m\n")
    
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    start_web_server()
