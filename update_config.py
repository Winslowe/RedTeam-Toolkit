import re

with open('Web_Dashboard.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_tools = '''TOOLS_CONFIG = [
    {
        "category": "C2 Framework & Evasion",
        "icon": "fa-skull-crossbones",
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
                "id": "sigthief",
                "name": "SigThief (Dijital İmza Çalma)",
                "path": "AV Evasion/SigThief.py",
                "desc": "Orijinal ve güvenilir bir programdan (Örn: Microsoft imzalı bir .exe) dijital imza sertifikasını kopyalar ve zararlı Payload'ınıza yapıştırır. Bu, Güvenlik Duvarlarını ve EDR/AV yazılımlarını atlatmak için harika bir yoldur.",
                "inputs": [
                    {"name": "arg1", "type": "text", "placeholder": "örn: C:\\\\Windows\\\\explorer.exe", "label": "Orijinal (İmzalı) EXE Yolu"},
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
        "category": "Pentest Automation",
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
]'''

start = content.find('TOOLS_CONFIG = [')
end = content.find('@app.before_request')

new_content = content[:start] + new_tools + '\n\n' + content[end:]

with open('Web_Dashboard.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('TOOLS_CONFIG updated successfully.')
