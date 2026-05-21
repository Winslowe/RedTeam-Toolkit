#!/usr/bin/env python3
"""
Web Dashboard for The Ultimate Pentest Arsenal - ELITE VERSION
==============================================================
Tüm araçları destekleyen, Sidebar tasarımlı profesyonel Flask sunucusu.
"""
import os
import sys
import subprocess
import json
import traceback
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Tüm araçların kategorileri ve gereksinim duydukları inputlar (Detaylı Açıklamalarla)
TOOLS_CONFIG = [
    {
        "category": "Elite & Automation",
        "icon": "fa-robot",
        "tools": [
            {
                "id": "autopwn",
                "name": "Auto-Pwn (Otopilot Sızma Motoru)",
                "path": "Auto_Pwn.py",
                "desc": "Belirttiğiniz hedef IP adresi üzerinde tam otomatik bir sızma testi (Pentest) gerçekleştirir. Önce açık portları tarar (Nmap stili), ardından 21 (FTP), 22 (SSH) veya 80 (HTTP) gibi kritik portlar bulduğunda otomatik olarak uygun Exploit veya Brute-Force araçlarını sırasıyla çalıştırarak sistemi ele geçirmeye çalışır.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "örn: 192.168.1.5", "label": "Hedef IP"},
                    {"name": "arg2", "type": "text", "placeholder": "Wordlist Yolu (Opsiyonel)", "label": "Kullanılacak Wordlist"}
                ]
            }
        ]
    },
    {
        "category": "OSINT (Açık Kaynak İstihbarat)",
        "icon": "fa-search",
        "tools": [
            {
                "id": "email_harvest",
                "name": "Email Harvester",
                "path": "OSINT/Email_Harvester.py",
                "desc": "Saldırı öncesi bilgi toplama aşamasında kullanılır. Hedef kuruma ait sızmış, internette dolaşan e-posta adreslerini arama motorları üzerinden tarayarak listeler. Oltalama (Phishing) saldırıları için kritik bir adımdır.",
                "inputs": [{"name": "arg1", "type": "text", "placeholder": "örn: example.com", "label": "Hedef Domain"}]
            },
            {
                "id": "whois_lookup",
                "name": "Whois Lookup",
                "path": "OSINT/Whois_Lookup.py",
                "desc": "Hedef domainin tescil bilgilerini, sahibini, oluşturulma tarihini ve hangi sunucularda (NameServer) barındığını gösteren detaylı bir analiz raporu sunar.",
                "inputs": [{"name": "arg1", "type": "text", "placeholder": "örn: example.com", "label": "Hedef Domain"}]
            }
        ]
    },
    {
        "category": "Network Recon (Ağ Keşfi)",
        "icon": "fa-network-wired",
        "tools": [
            {
                "id": "dns_enum",
                "name": "DNS Enumerator & Subdomain Tarayıcı",
                "path": "Network Recon/DNS_Enumerator.py",
                "desc": "Hedef alan adının arka planındaki tüm DNS kayıtlarını (A, MX, TXT vb.) çeker ve potansiyel alt alan adlarını (subdomain) tespit eder.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "örn: example.com", "label": "Domain"},
                    {"name": "arg2", "type": "text", "placeholder": "", "label": "Wordlist Yolu (Opsiyonel)"}
                ]
            },
            {
                "id": "net_scan",
                "name": "Local Network Scanner",
                "path": "Network Recon/Network_Scanner.py",
                "desc": "İç ağınızdaki (LAN) tüm cihazların IP ve MAC adreslerini saniyeler içinde tarar. Hedefleri belirlemek için ilk kullanılması gereken ağ aracıdır.",
                "inputs": [{"name": "arg1", "type": "text", "placeholder": "örn: 192.168.1.0/24", "label": "Hedef Ağ (CIDR Formatı)"}]
            },
            {
                "id": "arp_spoof",
                "name": "ARP Spoofer (MITM)",
                "path": "Network Recon/ARP_Spoofer.py",
                "desc": "Kurban ile modem arasındaki trafiği manipüle ederek araya girmenizi (Man-in-the-Middle) sağlar. Dikkat: Bu işlem arka planda çalışmaya devam eder ve manuel durdurulması gerekir.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "örn: 192.168.1.10", "label": "Kurban IP Adresi"},
                    {"name": "arg2", "type": "text", "placeholder": "örn: 192.168.1.1", "label": "Modem (Gateway) IP"}
                ]
            }
        ]
    },
    {
        "category": "Web Exploitation",
        "icon": "fa-globe",
        "tools": [
            {
                "id": "cms_scan",
                "name": "CMS Zafiyet Tarayıcı",
                "path": "Web Exploitation/CMS_Scanner.py",
                "desc": "Verilen web sitesinin WordPress, Joomla veya Drupal gibi bir altyapı kullanıp kullanmadığını anlar, versiyon bilgisini çıkarır ve bilinen zaafiyetli eklentileri arar.",
                "inputs": [{"name": "arg1", "type": "text", "placeholder": "örn: http://example.com", "label": "Hedef Web Sitesi (URL)"}]
            },
            {
                "id": "dir_brute",
                "name": "Directory Bruteforcer (DirBuster)",
                "path": "Web Exploitation/Directory_Bruteforcer.py",
                "desc": "Web sunucusundaki gizli klasörleri, unutulmuş yedek dosyalarını (backup.zip vb.) ve yetkisiz erişime açık panelleri kaba kuvvet (sözlük saldırısı) ile tespit eder.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "örn: http://example.com", "label": "Hedef URL"},
                    {"name": "arg2", "type": "text", "placeholder": "wordlists/common.txt", "label": "Wordlist Yolu"}
                ]
            },
            {
                "id": "sqli_test",
                "name": "SQL Injection (SQLi) Tester",
                "path": "Web Exploitation/SQLi_Tester.py",
                "desc": "Veritabanı sızıntısına yol açan SQL Injection hatalarını test etmek için verilen URL parametrelerine özel saldırı vektörleri gönderir.",
                "inputs": [{"name": "arg1", "type": "text", "placeholder": "örn: http://example.com/page?id=1", "label": "Zafiyetli Olabilecek URL"}]
            },
            {
                "id": "xss_test",
                "name": "XSS (Cross-Site Scripting) Scanner",
                "path": "Web Exploitation/XSS_Scanner.py",
                "desc": "Kullanıcı girdilerinin temizlenmediği noktalarda çalışan kötü amaçlı JavaScript kodlarını (XSS) tespit etmek için tarama yapar.",
                "inputs": [{"name": "arg1", "type": "text", "placeholder": "örn: http://example.com/search?q=", "label": "Arama veya Girdi URL'si"}]
            }
        ]
    },
    {
        "category": "Password Cracking",
        "icon": "fa-key",
        "tools": [
            {
                "id": "ssh_brute",
                "name": "SSH Bruteforce",
                "path": "Password Cracking/SSH_Bruteforce.py",
                "desc": "Linux/Sunucu sistemlerine izinsiz giriş yapmak amacıyla, SSH servisine (Port 22) belirtilen kelime listesi (wordlist) ile kaba kuvvet saldırısı düzenler.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "örn: 192.168.1.10", "label": "Sunucu IP Adresi"},
                    {"name": "arg2", "type": "text", "placeholder": "örn: root", "label": "Kullanıcı Adı"},
                    {"name": "arg3", "type": "text", "placeholder": "wordlists/passwords.txt", "label": "Wordlist Yolu"}
                ]
            },
            {
                "id": "ftp_brute",
                "name": "FTP Bruteforce",
                "path": "Password Cracking/FTP_Bruteforce.py",
                "desc": "Dosya transfer sunucularına (FTP - Port 21) izinsiz erişim sağlamak için parola tahmin etme saldırısı yapar.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "örn: 192.168.1.10", "label": "Sunucu IP Adresi"},
                    {"name": "arg2", "type": "text", "placeholder": "örn: admin", "label": "Kullanıcı Adı"},
                    {"name": "arg3", "type": "text", "placeholder": "wordlists/passwords.txt", "label": "Wordlist Yolu"}
                ]
            },
            {
                "id": "hash_crack",
                "name": "Offline Hash Cracker",
                "path": "Password Cracking/Hash_Cracker.py",
                "desc": "Sistemlerden sızdırılmış (ele geçirilmiş) şifreli metinlerin (MD5, SHA1, SHA256) orijinal hallerini, milyonlarca kelimenin bulunduğu dosyalarla eşleştirerek çözer.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "örn: 5d41402abc4b2a76b9719d911017c592", "label": "Kırılacak Hash Metni"},
                    {"name": "arg2", "type": "text", "placeholder": "wordlists/passwords.txt", "label": "Wordlist Yolu"}
                ]
            }
        ]
    },
    {
        "category": "Social Engineering",
        "icon": "fa-user-secret",
        "tools": [
            {
                "id": "phishing",
                "name": "Phishing (Oltalama) Server",
                "path": "Social Engineering/Phishing_Server.py",
                "desc": "Hedef kullanıcıyı kandırmak için sahte bir kurumsal giriş ekranı oluşturur. Kurban kullanıcı adı ve şifresini girdiğinde bunları kaydeder, Telegram botunuza gönderir ve kurbanı orijinal siteye yönlendirir.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "örn: 8080", "label": "Dinlenecek Port"},
                    {"name": "arg2", "type": "text", "placeholder": "örn: https://google.com", "label": "Orijinal (Yönlendirilecek) URL"},
                    {"name": "arg3", "type": "text", "placeholder": "örn: Kurumsal Ağ Girişi", "label": "Sahte Sayfa Başlığı"}
                ]
            }
        ]
    }
]

@app.route('/')
def index():
    # JSON objesini HTML içerisine render etmek için yolluyoruz
    return render_template('index.html', tools_config=json.dumps(TOOLS_CONFIG))

@app.route('/api/run', methods=['POST'])
def api_run():
    data = request.json
    tool_id = data.get('tool_id')
    args_dict = data.get('args', {})
    
    # Tool'u bul
    target_tool = None
    for category in TOOLS_CONFIG:
        for tool in category['tools']:
            if tool['id'] == tool_id:
                target_tool = tool
                break
        if target_tool: break
        
    if not target_tool:
        return jsonify({"status": "error", "output": "Araç bulunamadı!"})
        
    script_path = os.path.join(base_dir, target_tool['path'])
    if not os.path.exists(script_path):
        return jsonify({"status": "error", "output": f"Dosya bulunamadı: {target_tool['path']}"})
        
    # Parametreleri listeye çevir (arg1, arg2...)
    cmd_args = []
    # inputs sayısına göre argüman bekle
    for req_in in target_tool.get('inputs', []):
        val = args_dict.get(req_in['name'], "").strip()
        if val:
            cmd_args.append(val)
            
    # Phishing Server gibi sürekli arka planda çalışanları özel olarak ayır
    if tool_id == "phishing":
        cmd = [sys.executable, script_path] + cmd_args
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        port = cmd_args[0] if len(cmd_args)>0 else "8080"
        return jsonify({"status": "success", "output": f"[*] Phishing Server arka planda başlatıldı!\n[+] Adres: http://localhost:{port}/\n[+] Bildirimler (Notifier.py) aktifse şifreler size iletilecektir."})

    cmd = [sys.executable, script_path] + cmd_args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout + "\n" + result.stderr
        return jsonify({"status": "success", "output": output})
    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "output": "İşlem 120 saniyeyi aştığı için sonlandırıldı."})
    except Exception as e:
        return jsonify({"status": "error", "output": f"Hata oluştu:\n{traceback.format_exc()}"})

def start_web_server(port=5000):
    print(f"\n\033[92m[*] Premium Web Dashboard Başlatılıyor...\033[0m")
    print(f"\033[96m[+] Tarayıcınızdan şu adrese gidin:\033[0m \033[4mhttp://127.0.0.1:{port}/\033[0m")
    print(f"\033[90m(Web arayüzünü kapatmak için terminalde CTRL+C yapın)\033[0m\n")
    
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    start_web_server()
