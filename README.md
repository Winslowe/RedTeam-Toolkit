<h1 align="center">🛡️ The Ultimate Pentest Arsenal v5.0</h1>

<p align="center">
  <strong>Gelişmiş, Kapsamlı ve Tam Otomatik Sızma Testi ve Red Team Araç Seti</strong>
</p>

## 📌 Proje Hakkında
Bu proje, sızma testleri, siber güvenlik eğitimleri ve Red Team operasyonları için geliştirilmiş çok amaçlı bir çerçevedir (Framework). Ağ taramalarından gelişmiş Web zafiyet analizlerine, AV (Antivirüs) Evasion tekniklerinden gelişmiş Command & Control (C2) sistemlerine kadar bir siber güvenlik uzmanının ihtiyaç duyabileceği **26 farklı aracı** tek bir merkezden yönetmenizi sağlar.

Projenin en büyük avantajı, hiçbir aracı çalıştırırken karmaşık komut satırı parametreleri (`--ip`, `--port`) girmenize gerek kalmadan, tüm modüllerin size **etkileşimli bir sihirbaz (Wizard)** aracılığıyla sorular sorarak çalışmasıdır.

---

## 🚀 Özellikler & Modüller

### 🌐 1. OSINT (Açık Kaynak İstihbarat)
* **Email Harvester:** Hedef domain için internetten (Google vb.) kurum e-posta adreslerini toplar.
* **Whois Lookup:** Domain sahibi, registrar, name server ve tarihsel kayıt bilgilerini sorgular.

### 🎣 2. Social Engineering (Sosyal Mühendislik)
* **Phishing Server:** Hızlıca sahte bir login (giriş) sayfası başlatır ve girilen kimlik bilgilerini anında kaydeder. Kurbanları başarılı giriş sonrası gerçek siteye yönlendirir.

### 🔑 3. Privilege Escalation (Hak Yükseltme)
* **Linux / Windows PrivEsc Checkers:** Sistemde yetki yükseltmeye (Root/SYSTEM) olanak tanıyabilecek yanlış yapılandırmaları, cron görevlerini ve zayıf servisleri otomatik tarar.

### 🛡️ 4. AV Evasion (Antivirüs Atlatma)
* **Payload Obfuscator:** Python tabanlı zararlı yazılımlarınızı analiz edilmesini zorlaştırmak için obfuscate eder.
* **Shellcode Encoder:** RAW shellcode'larınızı XOR mantığıyla şifreleyerek statik antivirüs imzalarından kaçırır.

### 📡 5. Network Recon (Ağ Keşfi)
* **Network Scanner:** Yerel ağınızdaki (LAN) tüm cihazları ping ve ARP yardımıyla saniyeler içinde keşfeder.
* **DNS Enumerator & Subdomain Brute-Force:** Multi-threading mimarisiyle hedef alan adının tüm DNS kayıtlarını ve alt alan adlarını bulur.
* **ARP Spoofer:** Ortadaki Adam (MitM) saldırısı gerçekleştirerek hedef trafiği kendi üzerinize yönlendirir.

### 🌐 6. Web Exploitation (Web İstismarı)
* **CMS Vulnerability Scanner:** Sitenin altyapısını (WordPress, Joomla, Drupal) tespit edip zafiyet taraması yapar.
* **SQLi Tester:** Hedef URL üzerinde Error-Based ve Time-Based (Gecikmeli) SQL Injection taraması yapar.
* **XSS Scanner:** Gelişmiş payload listesiyle tarayıcı tabanlı Reflected XSS açıklarını tespit eder.
* **Directory Bruteforcer:** Sunucuda gizli kalmış yedek dosyalarını ve admin panellerini bulur.
* **LFI Scanner:** Local File Inclusion zafiyetlerini arayarak sunucu içi dosyaları (ör: `/etc/passwd`) okumayı dener.

### 🔓 7. Password Cracking (Parola Kırma)
* **Multi Hash Cracker:** MD5, SHA1, SHA256 ve NTLM hash türlerini çok çekirdekli (Multi-Processing) dictionary attack ile kırar.
* **ZIP Password Cracker:** Şifreli ZIP dosyalarını bellekte (RAM) kırarak maksimum hıza ulaşır.
* **SSH & FTP Bruteforce:** Uzak sunuculara otomatik parola denemeleri yapar.
* **Wordlist Generator:** Hedef kişinin ilgi alanlarına özel şifre listeleri (Wordlist) üretir.

### 💻 8. Post-Exploitation (Sızma Sonrası İstismar)
* **Reverse Shell Generator:** 12 farklı dilde (Python, Bash, PowerShell vb.) anında ters bağlantı komutları üretir.
* **Credential Harvester:** Ele geçirilen Windows makinelerdeki kayıtlı WiFi şifrelerini çeker.
* **Advanced Keylogger:** Kurbanın bastığı tuşları **aktif pencere başlıklarıyla** birlikte kaydeder.
* **Screenshot Grabber & Data Exfiltrator:** Hedef cihazın ekran görüntüsünü alır ve hassas verileri gizlice sızdırır.
* **Log Cleaner & Persistence:** Sistemdeki izlerinizi (logları) siler ve başlangıç kayıtlarına eklenerek kalıcılık sağlar.

### 📶 9. Wireless Attacks (Kablosuz Ağ Saldırıları)
* **Evil Twin:** Kurbanın ağıyla aynı isimde sahte bir Wi-Fi ağı oluşturarak "Captive Portal" üzerinden şifre çalar.

### ☠️ 10. C2 Framework & Stealth Dropper
* **Payload Builder:** Tek tıklamayla, **Anti-VM, Anti-Sandbox ve Anti-Debugging** özelliklerine sahip, Windows Defender'ı atlatan Nuitka derlemeli Native EXE üretir.
* **EXE Disguise (Kılık Değiştirme):** Ürettiğiniz EXE zararlısını RLO (Right-to-Left Override) taktiğiyle **sahte bir PNG/PDF** dosyasına dönüştürür.
* **Listener:** C2 Server üzerinden kurbanların bilgisayarlarına bağlanmanızı, veri indirip göndermenizi sağlar.

### 📊 11. Reporting (Raporlama)
* **HTML Report Generator:** Yapılan tarama ve tespit edilen bulguları derleyerek profesyonel görünümlü, renk kodlu ve yönetici özetli bir HTML pentest raporuna dönüştürür.

---

## 🛠️ Kurulum ve Kullanım

Sistemi kullanabilmek için Python 3.8 veya üzeri bir sürümün yüklü olması gerekmektedir.

### Hızlı Kurulum (Tavsiye Edilen)
**Windows için:**
Projeyi indirdiğiniz klasörde `kurulum.bat` dosyasına çift tıklamanız yeterlidir. Tüm bağımlılıklar otomatik kurulacak ve program başlatılacaktır.

**Linux / Kali Linux için:**
Terminali açıp proje dizinine girin ve aşağıdaki komutları çalıştırın:
```bash
chmod +x install.sh
./install.sh
```

### Manuel Kurulum
Eğer kurulum scriptlerini kullanmak istemezseniz:
```bash
pip install -r requirements.txt
python RedTeam_C2.py
```

---

## ⚠️ Yasal Uyarı
Bu proje tamamen **eğitim, akademik araştırma ve yasal sızma testi (penetration testing)** amaçlarıyla geliştirilmiştir. 
Bu araçların izin alınmamış sistemlerde (yetkisiz) kullanılması yasa dışıdır. Geliştiriciler, bu yazılımın kötüye kullanılmasından kaynaklanabilecek yasal sorunlardan veya doğabilecek zararlardan kesinlikle sorumlu tutulamaz. Yazılımı kullanan kişi, tüm yasal sorumluluğu kabul etmiş sayılır.
