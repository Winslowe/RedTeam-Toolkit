const moduleConfig = {
    // 01 Antivirus Atlatma
    "Payload_Obfuscator.py": {
        icon: "🛡️", desc: "Zararlı yazılımın (payload) imzasını değiştirerek antivirüs (AV) taramalarından kaçmasını sağlar. Temel bir gizlenme aracıdır.",
        params: [{name: "Orijinal Dosya", placeholder: "payload.py"}, {name: "Çıktı Dosyası", placeholder: "obf_payload.py"}]
    },
    "Process_Injector.py": {
        icon: "💉", desc: "Zararlı kodları (shellcode) çalışan yasal bir sistem sürecine (örn: explorer.exe) enjekte ederek tespit edilmeyi zorlaştırır.",
        params: [{name: "Hedef Süreç PID", placeholder: "1234"}, {name: "Shellcode Dosyası", placeholder: "shellcode.bin"}]
    },
    "Shellcode_Encoder.py": {
        icon: "🔄", desc: "Çıplak shellcode'u şifreleyerek veya kodlayarak bellek içi taramalardan gizler.",
        params: [{name: "Raw Shellcode Dosyası", placeholder: "raw.bin"}, {name: "Çıktı Dosyası", placeholder: "encoded.bin"}]
    },
    "SigThief.py": {
        icon: "📜", desc: "Yasal bir programın (örn: Microsoft aracı) dijital imzasını kopyalayıp zararlı yazılıma yapıştırır.",
        params: [{name: "İmzalı Dosya (Kaynak)", placeholder: "orijinal.exe"}, {name: "Hedef Dosya", placeholder: "zararli.exe"}]
    },

    // 02 Zafiyet Gelistirme (Buffer Overflow)
    "1_Fuzzing.py": {
        icon: "💥", desc: "Hedef servisin hafızasını taşırmak için giderek artan boyutlarda veri gönderir. Servisin çöktüğü bayt sınırını tespit eder.",
        params: [{name: "Hedef IP", placeholder: "192.168.1.5"}, {name: "Hedef Port", placeholder: "21"}]
    },
    "2_Offset.py": {
        icon: "📏", desc: "EIP yazmacının tam olarak hangi byte'ta (offset) üzerine yazıldığını bulur.",
        params: [{name: "Hedef IP", placeholder: "192.168.1.5"}, {name: "Hedef Port", placeholder: "21"}, {name: "Offset Deseni Uzunluğu", placeholder: "2000"}]
    },
    "3_Badchars.py": {
        icon: "🛑", desc: "Zafiyet sömürüsünü bozabilecek kötü karakterleri (badchars) tespit eder.",
        params: [{name: "Hedef IP", placeholder: "192.168.1.5"}, {name: "Hedef Port", placeholder: "21"}]
    },
    "4_Exploit.py": {
        icon: "🎯", desc: "Buffer Overflow zafiyetini tetikleyip hedefe zararlı shellcode gönderir.",
        params: [{name: "Hedef IP", placeholder: "192.168.1.5"}, {name: "Hedef Port", placeholder: "21"}]
    },

    // 03 Guvenlik Duvari Atlatma
    "1_Encrypted_Reverse_Shell.py": {
        icon: "🔏", desc: "Güvenlik duvarı (Firewall) sistemlerini atlatmak için ağ trafiğini AES/RSA ile şifreleyen bir arka kapı oluşturur.",
        params: [{name: "Dinleyici IP (LHOST)", placeholder: "192.168.1.10"}, {name: "Port (LPORT)", placeholder: "4444"}]
    },
    "2_Listener.py": {
        icon: "🎧", desc: "Şifrelenmiş veya tünellenmiş bağlantıları karşılayan güvenli dinleyici.",
        params: [{name: "Dinlenecek Port", placeholder: "4444"}]
    },
    "3_HTTP_Tunnel.py": {
        icon: "🚇", desc: "Zararlı trafiği normal web trafiği (HTTP 80/443) gibi göstererek ağ kısıtlamalarını aşar.",
        params: [{name: "Hedef IP", placeholder: "192.168.1.5"}, {name: "Tünel Portu", placeholder: "8080"}]
    },
    "4_Port_Scanner.py": {
        icon: "🔍", desc: "Güvenlik duvarı arkasındaki açık portları tespit etmek için gizli (stealth) taramalar yapar.",
        params: [{name: "Hedef IP veya Subnet", placeholder: "192.168.1.5"}]
    },

    // 04 Ag Kesif Araclari
    "ARP_Spoofer.py": {
        icon: "🎭", desc: "Ağdaki cihazların ARP tablolarını zehirleyerek (Ortadaki Adam - MITM) ağ trafiğini dinler.",
        params: [{name: "Hedef IP (Kurban)", placeholder: "192.168.1.5"}, {name: "Gateway IP (Modem)", placeholder: "192.168.1.1"}]
    },
    "DNS_Enumerator.py": {
        icon: "🌐", desc: "Hedef alan adının alt alan adlarını (subdomain), mail sunucularını ve DNS kayıtlarını çıkarır.",
        params: [{name: "Hedef Domain", placeholder: "ornek.com"}]
    },
    "DNS_Server_Listener.py": {
        icon: "📡", desc: "Ağda DNS isteklerini yakalar veya sahte DNS yanıtları vererek kurbanları sahte sitelere yönlendirir.",
        params: [{name: "Arayüz", placeholder: "eth0"}]
    },
    "Network_Scanner.py": {
        icon: "🗺️", desc: "Ağdaki tüm aktif cihazları, MAC adreslerini ve işletim sistemlerini haritalandırır.",
        params: [{name: "Hedef Alt Ağ (CIDR)", placeholder: "192.168.1.0/24"}]
    },

    // 05 Acik Kaynak Istihbarat
    "Email_Harvester.py": {
        icon: "📧", desc: "Arama motorları ve veri sızıntısı platformlarını kullanarak bir kuruma ait e-posta adreslerini toplar.",
        params: [{name: "Hedef Domain", placeholder: "ornek.com"}]
    },
    "Whois_Lookup.py": {
        icon: "🕵️", desc: "Alan adının sahibini, kayıt tarihlerini, sunucu IP'lerini ve iletişim bilgilerini sorgular.",
        params: [{name: "Hedef Domain veya IP", placeholder: "ornek.com"}]
    },

    // 06 Sifre Kirici Araclar
    "FTP_Bruteforce.py": {
        icon: "📁", desc: "FTP sunucularına yönelik şifre kaba kuvvet (Brute-Force) saldırısı gerçekleştirir.",
        params: [{name: "Hedef IP", placeholder: "192.168.1.10"}, {name: "Kullanıcı Adı", placeholder: "admin"}, {name: "Wordlist Yolu", placeholder: "wordlist.txt"}]
    },
    "Hash_Cracker.py": {
        icon: "🔓", desc: "MD5, SHA1, SHA256 gibi şifre hashlerini wordlist kullanarak çevrimdışı kırar.",
        params: [{name: "Kırılacak Hash", placeholder: "5d41402abc..."}, {name: "Wordlist", placeholder: "rockyou.txt"}]
    },
    "Hash_Identifier.py": {
        icon: "🏷️", desc: "Elinizdeki şifreli metnin hangi algoritma (MD5, NTLM vb.) ile şifrelendiğini analiz eder.",
        params: [{name: "Bilinmeyen Hash", placeholder: "e10adc39..."}]
    },
    "SSH_Bruteforce.py": {
        icon: "🔑", desc: "Linux sunucularına uzaktan erişim (SSH) parolalarını kırmak için kullanılır.",
        params: [{name: "Hedef IP", placeholder: "192.168.1.10"}, {name: "Kullanıcı Adı", placeholder: "root"}, {name: "Wordlist Yolu", placeholder: "wordlist.txt"}]
    },
    "Wordlist_Generator.py": {
        icon: "📝", desc: "Kişiye veya kuruma özel kelime kombinasyonlarıyla özel şifre listeleri (Wordlist) oluşturur.",
        params: [{name: "Minimum Uzunluk", placeholder: "6"}, {name: "Maksimum Uzunluk", placeholder: "10"}, {name: "Karakter Seti", placeholder: "abc123"}]
    },
    "Zip_Cracker.py": {
        icon: "🗜️", desc: "Parola korumalı ZIP arşivlerinin şifresini brute-force ile kırar.",
        params: [{name: "Hedef ZIP Dosyası", placeholder: "gizli.zip"}, {name: "Wordlist", placeholder: "rockyou.txt"}]
    },

    // 07 Sizma Sonrasi Taktikler
    "Credential_Harvester.py": {
        icon: "🎣", desc: "Hedef sistemdeki kayıtlı tarayıcı şifrelerini, WiFi parolalarını ve kimlik bilgilerini toplar.",
        params: [{name: "Hedef Dosya Çıktısı", placeholder: "credentials.txt"}]
    },
    "Data_Exfiltrator.py": {
        icon: "📤", desc: "Hedef sistemden toplanan verileri (veri sızdırma) gizli tünellerle saldırgana aktarır.",
        params: [{name: "Sızdırılacak Dosya", placeholder: "gizli_belge.pdf"}, {name: "Hedef IP (Saldırgan)", placeholder: "192.168.1.10"}]
    },
    "DNS_Exfiltrator.py": {
        icon: "📡", desc: "Ağdaki verileri DNS sorgularının içerisine saklayarak (Firewall atlatarak) dışarı sızdırır.",
        params: [{name: "Sızdırılacak Dosya", placeholder: "data.txt"}, {name: "Saldırgan DNS", placeholder: "evil.com"}]
    },
    "Log_Cleaner.py": {
        icon: "🧹", desc: "Sisteme bırakılan izleri yok etmek için Windows Event Log'ları (Olay Günlükleri) veya Linux loglarını temizler.",
        params: [{name: "İşlem Türü", placeholder: "all (Tüm izleri sil)"}]
    },
    "Persistence_Installer.py": {
        icon: "⚓", desc: "Hedef sistem yeniden başlatılsa bile zararlı yazılımın tekrar çalışmasını (Kalıcılık) sağlar.",
        params: [{name: "Zararlı Dosya Yolu", placeholder: "C:\\Windows\\Temp\\backdoor.exe"}]
    },
    "Reverse_Shell_Gen.py": {
        icon: "🐍", desc: "Farklı dillere (Python, Bash, PowerShell) özel Reverse Shell kodları üretir.",
        params: [{name: "Dinleyici IP (LHOST)", placeholder: "192.168.1.10"}, {name: "Dinleyici Port (LPORT)", placeholder: "4444"}]
    },
    "Screenshot_Grabber.py": {
        icon: "📸", desc: "Kurbanın haberi olmadan ekran görüntüsünü çeker.",
        params: [{name: "Çıktı Dosyası", placeholder: "ekran.png"}]
    },
    "Simple_Keylogger.py": {
        icon: "⌨️", desc: "Klavye vuruşlarını kaydederek şifreleri ve mesajları toplar.",
        params: [{name: "Kayıt Dosyası", placeholder: "keylog.txt"}]
    },

    // 08 Yetki Yukseltme
    "Linux_PrivEsc_Checker.py": {
        icon: "🐧", desc: "Linux sistemlerde zafiyetleri ve yanlış yapılandırmaları tarayarak ROOT yetkisine ulaşmanın yollarını arar.",
        params: [{name: "Çıktı Log Dosyası", placeholder: "privesc_report.txt"}]
    },

    // 09 Raporlama
    "Report_Generator.py": {
        icon: "📊", desc: "Yapılan saldırı ve tarama sonuçlarını profesyonel bir sızma testi raporuna (HTML/PDF) dönüştürür.",
        params: [{name: "Rapor Adı", placeholder: "pentest_raporu"}]
    },

    // 10 Sosyal Muhendislik
    "Phishing_Server.py": {
        icon: "🎣", desc: "Sahte bir giriş sayfası (Örn: Instagram, Banka) barındıran bir oltalama sunucusu başlatır.",
        params: [{name: "Port", placeholder: "80"}]
    },

    // 11 Gizli Zararli Olusturucu
    "stub_template.py": {
        icon: "🦠", desc: "C2 sunucusuna bağlanan gelişmiş özellikleri barındıran zombi ajan taslağıdır.",
        params: [{name: "LHOST", placeholder: "192.168.1.10"}]
    },

    // 12 Web Zafiyet Araclari
    "CMS_Scanner.py": {
        icon: "🔍", desc: "WordPress, Joomla vb. içerik yönetim sistemlerindeki bilinen zafiyetleri (plugin, tema) tespit eder.",
        params: [{name: "Hedef URL", placeholder: "http://hedef.com"}]
    },
    "Directory_Bruteforcer.py": {
        icon: "📂", desc: "Web sunucusundaki gizli klasörleri ve dosyaları (admin, backup, vb.) kaba kuvvet ile bulur.",
        params: [{name: "Hedef URL", placeholder: "http://hedef.com"}, {name: "Wordlist Yolu", placeholder: "wordlist.txt"}]
    },
    "LFI_Scanner.py": {
        icon: "📁", desc: "Local File Inclusion (Yerel Dosya Dahil Etme) zafiyetlerini test eder (Örn: /etc/passwd okuma).",
        params: [{name: "Hedef URL Parametresi", placeholder: "http://hedef.com/page?file="}]
    },
    "SQLi_Tester.py": {
        icon: "💉", desc: "Veritabanına SQL enjeksiyonu yapılabilecek URL parametrelerini otomatik test eder.",
        params: [{name: "Hedef URL", placeholder: "http://hedef.com/page?id=1"}]
    },
    "XSS_Scanner.py": {
        icon: "👾", desc: "Web sayfalarındaki girdi alanlarında (Arama Kutusu, Yorum vb.) Cross-Site Scripting zafiyeti arar.",
        params: [{name: "Hedef URL", placeholder: "http://hedef.com/search?q="}]
    },

    // 13 Kablosuz Ag Saldirilari
    "Evil_Twin.py": {
        icon: "📡", desc: "Gerçek bir Wi-Fi ağıyla aynı isimde sahte bir ağ (İkiz Şeytan) oluşturarak bağlanan cihazları hackler.",
        params: [{name: "Ağ Arayüzü (Interface)", placeholder: "wlan0"}, {name: "Sahte Ağ Adı (SSID)", placeholder: "Free_Starbucks_WiFi"}]
    }
};

window.moduleConfig = moduleConfig;
