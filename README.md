<div align="center">

# 💀 The Ultimate Pentest Arsenal (RedTeam C2 Karargahı)

**Profesyonel, Hepsi Bir Arada Siber Güvenlik, Otomasyon ve Kırmızı Takım (Red Team) Aracı**

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Elite%20APT-red.svg)]()
[![FUD](https://img.shields.io/badge/FUD%20Rate-0%2F70-success.svg)]()

*Bu proje yalnızca eğitim, sızma testi yetkilendirmesi olan profesyoneller ve etik hackerlar (White Hat) için geliştirilmiştir.*

---

</div>

## 📖 Proje Hakkında
Bu proje, standart bir script yığınından öte, tam teşekküllü bir **Komuta Kontrol Merkezi (C2)** ve **Pentest Otomasyon** (Auto-Pwn) aracıdır. Tüm sistemi **`C2_Karargah.py`** üzerinden tek bir noktadan yönetirsiniz.

---

## 🚀 KULLANIM KILAVUZU (Neyi Nasıl Kullanmalısınız?)

Sistemi başlatmak için terminalinizde şu komutu çalıştırın:
```bash
python C2_Karargah.py
```
Karşınıza efsanevi bir ASCII logosu ve Ana Menü çıkacaktır.

### 🔴 1. C2 Komuta Merkezi (Menü Seçeneği: 0)
Sistemin kalbidir. Kendi Zombi Botnet ağınızı kurmanızı sağlar. Bu menüye girdiğinizde 3 ana seçeneğiniz vardır:

#### 🟢 Payload Builder (Zararlı Yazılım Üretici)
- **Ne İşe Yarar?** Hedef bilgisayara göndereceğiniz `EXE` virüs dosyasını oluşturur.
- **Nasıl Kullanılır?** Kendi IP adresinizi ve Portunuzu (Örn: 443) girin. Araç arka planda C dilinde (Nuitka ile) **FUD (Anti-Virüslere yakalanmayan)**, AES-256 şifreli bir EXE üretir. İçerisindeki değişkenler her üretimde rastgele değiştiği için statik imzalara takılmaz.
- **Çıktı:** Dosya `Moduller/11_Gizli_Zararli_Olusturucu/` içine kaydedilir.

#### 🟢 Listener (Dinleyici & Botnet Yöneticisi)
- **Ne İşe Yarar?** Ürettiğiniz virüsü hedefe gönderdikten sonra, hedefin size bağlanmasını beklediğiniz ekrandır. Arka planda çalışır ve **aynı anda 50 kurbanı** (Multi-Session) destekler.
- **Nasıl Kullanılır?** Payload'ı oluştururken yazdığınız Portu (Örn: 443) yazıp dinlemeye başlayın.
- **Özel Shell Komutları (Kurban size bağlandığında C2 konsolunda kullanılır):**
  - `sessions` : Ağa düşen tüm zombileri listeler.
  - `interact 1` : 1 numaralı zombinin içine girer (Bağlantı kurar).
  - `background` : Zombinin içinden çıkıp ana dinleyiciye döner.
  - `!steal_passwords` : Kurbanın Chrome/Edge tarayıcısındaki tüm kayıtlı şifreleri çalıp (Decrypt edip) `Ganimetler/` klasörüne kaydeder.
  - `!screenshot` : Kurbanın bilgisayarından sessizce ekran görüntüsü alıp `Ganimetler/` klasörüne PNG olarak kaydeder.
  - `!keylog_start` : Hedefin klavyesini arka planda dinlemeye başlar.
  - `!keylog_dump` : Dinlenen klavye verilerini ekrana yazdırır.
  - `!persist` : Virüsü Windows Kayıt Defteri'ne gizlice ekler. Bilgisayar yeniden başlasa bile virüs otomatik açılır.
  - `!PANIK` : Kill-Switch. Acil bir durumda kurban bilgisayarındaki virüsü tamamen siler (Suicide modu), bağlantıları koparır ve logları yok eder.

#### 🟢 EXE Disguise (Kılık Değiştirme)
- **Ne İşe Yarar?** Oluşturduğunuz EXE virüsünü bir resim (`.png`, `.jpg`) veya belge (`.pdf`) gibi gösterir. Kurban dosyaya tıkladığında ekrana gerçek bir resim (Yem) açılırken, virüs arka planda çalışır.

---

### 🤖 2. Oto Sızma Aracı (Menü Seçeneği: 00)
- **Ne İşe Yarar?** Bir hedefin (IP Adresi) açık portlarını bulur ve o portlara uygun hack araçlarını (Brute Force, DirBuster, SQLi) **insan müdahalesi olmadan** otomatik çalıştırır.
- **Nasıl Kullanılır?** Menüden `00` seçin, hedef IP'yi verin ve arkanıza yaslanın. Çıktıyı detaylı bir `.txt` raporu olarak kaydeder ve telefonunuza "İşlem bitti" mesajı atar.

---

### 🛠️ 3. Sızma Testi Modülleri (Kategori 1'den 13'e kadar)
Ana menüde listelenen 13 farklı kategori, manuel sızma testleri (Pentest) için tasarlanmıştır. İstediğiniz numarayı (Örn: `1`) tuşlayarak kategoriye girin.
- **01_Antivirus_Atlatma:** Mevcut zararlıları gizleme araçları.
- **04_Ag_Kesif_Araclari:** Hedef ağda nmap taramaları veya ARP Spoofing (Ortadaki Adam Saldırısı) yapmak için.
- **06_Sifre_Kirici_Araclar:** FTP, SSH gibi servislere Wordlist ile saldırı (Bruteforce) araçları.
- **10_Sosyal_Muhendislik:** Phishing (Oltalama) sunucusu başlatarak kurbanların şifrelerini çalma sayfası kurar.

---

## 📱 Bildirim Sistemi Kurulumu (Telegram/Discord)

Ağa yeni bir Zombi (Kurban) düştüğünde telefonunuza anında uyarı gelmesi için `Moduller/Sistem/config.json` dosyasını açıp kendi Telegram bilgilerinizi girmelisiniz:

```json
{
    "telegram_bot_token": "BOT_TOKEN_BURAYA",
    "telegram_chat_id": "CHAT_ID_BURAYA",
    "discord_webhook": "",
    "notifications_enabled": true
}
```

## ⚠️ Yasal Uyarı
Bu proje eğitim ve savunma amacıyla tasarlanmıştır. Bu araç setinin izin alınmamış sistemler üzerinde kullanılması yasa dışıdır. Geliştirici yasal veya cezai hiçbir sorumluluğu kabul etmez.
