<div align="center">

# 💀 The Ultimate Pentest Arsenal (RedTeam C2)

**Profesyonel, Hepsi Bir Arada Siber Güvenlik, Otomasyon ve Kırmızı Takım (Red Team) Aracı**

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![Status](https://img.shields.io/badge/Status-Elite-red.svg)]()

*Bu proje yalnızca eğitim, sızma testi (pentest) yetkilendirmesi olan profesyoneller ve etik hackerlar (White Hat) için geliştirilmiştir.*

---

</div>

## 📖 Proje Hakkında

**The Ultimate Pentest Arsenal**, dağınık haldeki siber güvenlik araçlarını (Nmap, DirBuster, Hydra, Metasploit vb. işlevlerini) tek bir merkezden, **Karanlık Mod (Dark Mode) Web Dashboard** veya **Terminal Sihirbazı** aracılığıyla yönetmenizi sağlayan devasa bir Red Team otomasyon aracıdır.

Sıfırdan tasarlanan **Askeri Düzey AES-256 Şifreli C2 (Command & Control)** mimarisi sayesinde, oluşturduğunuz Zararlı Yazılımlar (Payloads) hedef ağdaki modern Firewall ve IDS sistemlerini kolayca atlatır (Bypass).

## 🚀 Öne Çıkan "Elite" Özellikler

- **🤖 Auto-Pwn (Otopilot):** Tek bir IP adresi verin, arkaya yaslanın. Araç kendi kendine portları tarar, bulduğu servislere (HTTP, FTP, SSH) uygun zafiyet araçlarını zincirleme çalıştırır ve raporu sunar.
- **🌐 Flask Web Dashboard:** 26 farklı sızma testi aracını, komut satırı ezberlemeden, şık bir web tarayıcı arayüzünden (Sidebar, Interaktif Kartlar) yönetin.
- **🔒 AES-256 E2EE C2 Bağlantısı:** Hedef cihazlarla aranızdaki Reverse Shell iletişimi uçtan uca AES-256 ile şifrelenir. 
- **📱 Telegram & Discord Entegrasyonu:** Şifre mi kırıldı? Biri Phishing ağına mı düştü? Yoksa C2'ye yeni bir shell mi bağlandı? Sistem anında cebinize bildirim gönderir.
- **🛡️ Anti-VM & SmartScreen Bypass:** Nuitka ile C diline derlenen (Native EXE) payload'lar sayesinde, antivirüslerin (AV) statik analizlerinden ve Sandbox ortamlarından kurtulun.

---

## 🏗️ Mimari Şeması (Architecture)

Aşağıdaki şema, projenin modüllerinin birbiriyle nasıl haberleştiğini göstermektedir:

```mermaid
graph TD
    A[👨‍💻 Saldırgan / Güvenlik Uzmanı] -->|Terminal Sihirbazı| B(RedTeam_C2 Core)
    A -->|Web Tarayıcı :5000| W[🌐 Flask Web Dashboard]
    W <--> B
    
    B --> C{Saldırı Vektörleri}
    
    C -->|Bilgi Toplama| D[OSINT & Network Recon]
    D --> D1[Email, Whois, DNS, ARP Spoof]
    
    C -->|Zafiyet Analizi| E[Web Exploitation]
    E --> E1[CMS Scan, DirBrute, SQLi, XSS]
    
    C -->|Otomasyon| F[🤖 Auto-Pwn Motoru]
    F -->|Tarama + Exploit Zinciri| C
    
    C -->|Erişim Sağlama| G[Password Cracking & Phishing]
    G -->|Yakalanan Şifreler| T((📱 Telegram/Discord Bildirimi))
    
    C -->|Kalıcılık & Kontrol| H[AES-256 C2 Listener]
    H <==>|Uçtan Uca Şifreli Bağlantı| I[💀 Hedef Sistem / Kurban]
    
    I -->|Veri Sızdırma| H
```

---

## 🧰 Modüller ve İçerikleri

Proje içerisinde **26+** modül kategorize edilmiş durumdadır:

| Kategori | Araçlar | Açıklama |
| :--- | :--- | :--- |
| **OSINT** | `Email_Harvester`, `Whois_Lookup` | Alan adları ve hedefler hakkında açık kaynaklardan veri toplar. |
| **Network Recon** | `Network_Scanner`, `DNS_Enumerator`, `ARP_Spoofer` | LAN üzerinde cihaz tespiti, DNS analizi ve ağ trafiğini manipüle etme (MITM). |
| **Web Exploitation** | `CMS_Scanner`, `DirBrute`, `SQLi`, `XSS`, `LFI` | Web sunucularındaki kritik zafiyetleri ve gizli dosyaları analiz eder. |
| **Password Cracking** | `SSH_Brute`, `FTP_Brute`, `Hash_Cracker`, `Zip_Cracker` | Kritik servislere ve dosyalara yönelik kaba kuvvet saldırıları düzenler. |
| **Social Engineering**| `Phishing_Server` | Modern, log tutan ve bildirim gönderen sahte oltalama sunucusu. |
| **C2 & Evasion** | `Payload_Builder`, `C2_Listener`, `Obfuscator` | Antivirüslere yakalanmayan, AES-256 şifreli Reverse Shell oluşturucu ve dinleyici. |

---

## 💻 Kurulum ve Çalıştırma

The Ultimate Pentest Arsenal, tüm bağımlılıkları tek tuşla kurabilmeniz için özel scriptler içerir.

### Windows İçin
Dizindeki **`kurulum.bat`** dosyasına çift tıklayın veya terminalde çalıştırın:
```cmd
kurulum.bat
```

### Linux (Kali / Parrot) İçin
Terminali açın ve şu komutları girin:
```bash
chmod +x install.sh
./install.sh
```

### Projeyi Başlatma (Ana Menü)
Tüm araçları yöneteceğiniz merkezi çalıştırmak için:
```bash
python RedTeam_C2.py
```

Bu komuttan sonra karşınıza çıkan sihirbazdan:
- İstediğiniz aracı seçip **Terminal Sihirbazı** üzerinden parametreleri adım adım girebilirsiniz.
- Veya menüden **"13) Web Dashboard"** seçeneğini seçerek tarayıcınızdan muhteşem grafik arayüzüne bağlanabilirsiniz!

---

## ⚙️ Bildirim Ayarları (Config)

Projedeki oltalama (Phishing), otopilot (Auto-Pwn) veya yeni C2 kurban bağlantıları sırasında cebinize bildirim gelmesini istiyorsanız, proje dizininde oluşan `config.json` dosyasını şu şekilde düzenleyin:

```json
{
    "telegram_bot_token": "123456789:ABCdefGHIjklMNOpqrs",
    "telegram_chat_id": "12345678",
    "discord_webhook": "https://discord.com/api/webhooks/...",
    "notifications_enabled": true
}
```

---

## ⚠️ Yasal Uyarı

Bu proje **sadece** sistem yöneticileri, sızma testi (penetration testing) uzmanları ve siber güvenlik öğrencileri için eğitim/savunma amacıyla tasarlanmıştır.

Bu araç setinin izin alınmamış sistemler (kurumlar, kişiler veya sunucular) üzerinde kullanılması **yasa dışıdır**. Geliştirici, bu kodların kötüye kullanımından doğacak yasal veya cezai hiçbir sorumluluğu kabul etmez. Kullanıcı, aracı kullanırken bulunduğu ülkenin bilişim yasalarına uymakla yükümlüdür.

<div align="center">
  <br>
  <i>"Güvenlik bir yanılsama değil, sürekli bir savunma halidir."</i>
</div>
