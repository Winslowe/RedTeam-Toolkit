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

# Tüm araçların kategorileri ve gereksinim duydukları inputlar
TOOLS_CONFIG = [
    {
        "category": "Elite & Automation",
        "icon": "fa-robot",
        "tools": [
            {
                "id": "autopwn",
                "name": "Auto-Pwn (Otopilot)",
                "path": "Auto_Pwn.py",
                "desc": "Açık portları tarar ve hedefe uygun modülleri zincirleme çalıştırır.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "192.168.1.5", "label": "Hedef IP"},
                    {"name": "arg2", "type": "text", "placeholder": "Wordlist (Opsiyonel)", "label": "Wordlist Yolu"}
                ]
            }
        ]
    },
    {
        "category": "OSINT",
        "icon": "fa-search",
        "tools": [
            {
                "id": "email_harvest",
                "name": "Email Harvester",
                "path": "OSINT/Email_Harvester.py",
                "desc": "Hedef domain için açık kaynaklardan e-posta toplar.",
                "inputs": [{"name": "arg1", "type": "text", "placeholder": "example.com", "label": "Hedef Domain"}]
            },
            {
                "id": "whois_lookup",
                "name": "Whois Lookup",
                "path": "OSINT/Whois_Lookup.py",
                "desc": "Domain hakkında tescil ve sunucu bilgilerini getirir.",
                "inputs": [{"name": "arg1", "type": "text", "placeholder": "example.com", "label": "Hedef Domain"}]
            }
        ]
    },
    {
        "category": "Network Recon",
        "icon": "fa-network-wired",
        "tools": [
            {
                "id": "dns_enum",
                "name": "DNS Enumerator",
                "path": "Network Recon/DNS_Enumerator.py",
                "desc": "DNS kayıtlarını ve alt alan adlarını (subdomain) bulur.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "example.com", "label": "Domain"},
                    {"name": "arg2", "type": "text", "placeholder": "", "label": "Wordlist Yolu (Opsiyonel)"}
                ]
            },
            {
                "id": "net_scan",
                "name": "Network Scanner",
                "path": "Network Recon/Network_Scanner.py",
                "desc": "Belirtilen ağ aralığındaki cihazları (IP/MAC) bulur.",
                "inputs": [{"name": "arg1", "type": "text", "placeholder": "192.168.1.0/24", "label": "Hedef Ağ (CIDR)"}]
            },
            {
                "id": "arp_spoof",
                "name": "ARP Spoofer",
                "path": "Network Recon/ARP_Spoofer.py",
                "desc": "Kurban ile modem arasına girer (MITM). Uzun sürer, manuel durdurulur.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "192.168.1.10", "label": "Kurban IP"},
                    {"name": "arg2", "type": "text", "placeholder": "192.168.1.1", "label": "Modem IP"}
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
                "name": "CMS Scanner",
                "path": "Web Exploitation/CMS_Scanner.py",
                "desc": "WordPress, Joomla, Drupal altyapısını ve zafiyetlerini analiz eder.",
                "inputs": [{"name": "arg1", "type": "text", "placeholder": "http://example.com", "label": "Hedef URL"}]
            },
            {
                "id": "dir_brute",
                "name": "Directory Bruteforcer",
                "path": "Web Exploitation/Directory_Bruteforcer.py",
                "desc": "Gizli dizinleri ve dosyaları tespit eder.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "http://example.com", "label": "Hedef URL"},
                    {"name": "arg2", "type": "text", "placeholder": "wordlists/common.txt", "label": "Wordlist Yolu"}
                ]
            },
            {
                "id": "sqli_test",
                "name": "SQLi Tester",
                "path": "Web Exploitation/SQLi_Tester.py",
                "desc": "SQL Injection (SQLi) güvenlik açıklarını tespit eder.",
                "inputs": [{"name": "arg1", "type": "text", "placeholder": "http://example.com/page?id=1", "label": "Hedef URL (Parametreli)"}]
            },
            {
                "id": "xss_test",
                "name": "XSS Scanner",
                "path": "Web Exploitation/XSS_Scanner.py",
                "desc": "Cross-Site Scripting (XSS) açıklarını bulur.",
                "inputs": [{"name": "arg1", "type": "text", "placeholder": "http://example.com/search?q=", "label": "Hedef URL (Parametreli)"}]
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
                "desc": "SSH servisine sözlük saldırısı yapar.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "192.168.1.10", "label": "Hedef IP"},
                    {"name": "arg2", "type": "text", "placeholder": "root", "label": "Kullanıcı Adı"},
                    {"name": "arg3", "type": "text", "placeholder": "wordlists/passwords.txt", "label": "Wordlist Yolu"}
                ]
            },
            {
                "id": "ftp_brute",
                "name": "FTP Bruteforce",
                "path": "Password Cracking/FTP_Bruteforce.py",
                "desc": "FTP servisine sözlük saldırısı yapar.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "192.168.1.10", "label": "Hedef IP"},
                    {"name": "arg2", "type": "text", "placeholder": "admin", "label": "Kullanıcı Adı"},
                    {"name": "arg3", "type": "text", "placeholder": "wordlists/passwords.txt", "label": "Wordlist Yolu"}
                ]
            },
            {
                "id": "hash_crack",
                "name": "Hash Cracker",
                "path": "Password Cracking/Hash_Cracker.py",
                "desc": "MD5/SHA1/SHA256 şifre özetlerini wordlist ile kırar.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "5d41402abc4b2a76b9719d911017c592", "label": "Hash Metni"},
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
                "name": "Phishing Server",
                "path": "Social Engineering/Phishing_Server.py",
                "desc": "Sahte giriş portalı oluşturup girilen şifreleri kaydeder.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "8080", "label": "Dinlenecek Port"},
                    {"name": "arg2", "type": "text", "placeholder": "https://google.com", "label": "Yönlendirilecek Adres"},
                    {"name": "arg3", "type": "text", "placeholder": "Secure Portal", "label": "Sayfa Başlığı"}
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
