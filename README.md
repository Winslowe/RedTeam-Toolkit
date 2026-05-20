# 🛡️ Ultimate Pentest & Red Team Cheatsheet

Sızma testi uzmanları, güvenlik araştırmacıları ve Red Team üyeleri için hazırlanmış kapsamlı araç ve doküman deposu. Bu proje, eğitim amaçlı ve yasal güvenlik testlerinde kullanılmak üzere tasarlanmıştır.

## 📂 Modüller

1. **Firewall Bypass**: Antivirüs ve güvenlik duvarlarını atlatmak için şifreli reverse shell ve HTTP tünelleme araçları.
2. **Buffer Overflow**: Fuzzing, offset bulma ve bellek taşması zafiyetlerini sömürmek için temel scriptler.
3. **Privilege Escalation**: Linux ve Windows sistemlerde yetki yükseltme (PrivEsc) açıklarını tespit eden tarayıcılar.
4. **Web Exploitation**: SQL Injection ve XSS gibi yaygın web zafiyetlerini test etmek için otomatize araçlar.
5. **Password Cracking**: MD5 hash kırma ve ZIP dosyası parolalarını brute-force yöntemiyle çözme scriptleri.
6. **Network Recon**: Alt alan adı (subdomain) keşfi ve ARP Spoofing ile ağ analizi araçları.
7. **Post-Exploitation**: Sistemde tutunma, bilgi toplama (keylogger) ve veri sızdırma simülasyonları.
8. **AV Evasion**: Payload gizleme (obfuscation) ve shellcode şifreleme ile antivirüs atlatma yöntemleri.

## ⚠️ Yasal Uyarı

Bu araçlar ve kodlar **YALNIZCA EĞİTİM AMAÇLI** ve **YETKİLİ SIZMA TESTLERİ** için yazılmıştır. Herhangi bir sisteme izinsiz erişim sağlamak yasa dışıdır. Geliştirici, bu araçların kötüye kullanımından sorumlu tutulamaz.

## 🚀 Kullanım

Her modülün kendi klasörü altında ilgili Python/Bash/Bat scriptleri bulunmaktadır. Gerekli kütüphaneleri kurmak için:

```bash
pip install requests scapy pynput
```

*(Her aracın kullanımı kendi dosyasının içinde yorum satırı olarak belirtilmiştir.)*
