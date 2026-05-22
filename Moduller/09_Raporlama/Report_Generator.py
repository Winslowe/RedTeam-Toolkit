#!/usr/bin/env python3
"""
HTML Report Generator
=====================
Pentest sonuçlarını bir araya getirerek şık bir HTML raporu oluşturur.
"""
import os
import json
from datetime import datetime

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sızma Testi Raporu</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 0; }
        header { background-color: #2c3e50; color: #ecf0f1; padding: 20px; text-align: center; }
        .container { max-width: 1000px; margin: 20px auto; padding: 20px; background: #fff; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        h1 { margin: 0; }
        h2 { color: #e74c3c; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }
        .summary { display: flex; justify-content: space-around; margin-bottom: 30px; background: #ecf0f1; padding: 15px; border-radius: 5px; }
        .summary-box { text-align: center; }
        .summary-box span { display: block; font-size: 24px; font-weight: bold; color: #c0392b; }
        .finding { background: #fff; border-left: 5px solid #e74c3c; margin-bottom: 20px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        .finding h3 { margin-top: 0; color: #2c3e50; }
        .severity-high { color: #e74c3c; font-weight: bold; }
        .severity-medium { color: #f39c12; font-weight: bold; }
        .severity-low { color: #3498db; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #f8f9fa; }
        footer { text-align: center; padding: 20px; color: #7f8c8d; font-size: 14px; }
        code { background: #eee; padding: 2px 5px; border-radius: 3px; font-family: monospace; }
    </style>
</head>
<body>

<header>
    <h1>🛡️ The Ultimate Pentest Arsenal — Otomatik Rapor</h1>
    <p>Oluşturulma Tarihi: {date}</p>
</header>

<div class="container">
    <h2>📋 Yönetici Özeti</h2>
    <div class="summary">
        <div class="summary-box">
            <span>{total}</span> Toplam Bulgu
        </div>
        <div class="summary-box">
            <span style="color: #e74c3c;">{high}</span> Yüksek Risk
        </div>
        <div class="summary-box">
            <span style="color: #f39c12;">{medium}</span> Orta Risk
        </div>
        <div class="summary-box">
            <span style="color: #3498db;">{low}</span> Düşük Risk
        </div>
    </div>

    <h2>🔍 Detaylı Bulgular</h2>
    {findings_html}

</div>

<footer>
    <p>Bu rapor <b>Pentest-Cheatsheet</b> aracı tarafından otomatik üretilmiştir.</p>
</footer>

</body>
</html>
"""

def generate_report(json_data_path, output_html="Pentest_Report.html"):
    print("[*] Rapor oluşturuluyor...")
    
    # Örnek veri (Eğer JSON dosyası yoksa varsayılan verilerle demo rapor oluştur)
    findings = []
    if os.path.exists(json_data_path):
        try:
            with open(json_data_path, 'r', encoding='utf-8') as f:
                findings = json.load(f)
        except Exception as e:
            print(f"[-] JSON okuma hatası: {e}. Demo veri kullanılacak.")
            findings = get_demo_findings()
    else:
        print(f"[-] {json_data_path} bulunamadı. Demo rapor oluşturuluyor.")
        findings = get_demo_findings()

    # İstatistikler
    high = sum(1 for f in findings if f.get("severity") == "Yüksek")
    medium = sum(1 for f in findings if f.get("severity") == "Orta")
    low = sum(1 for f in findings if f.get("severity") == "Düşük")
    total = len(findings)

    # Bulguları HTML'e çevir
    findings_html = ""
    for f in findings:
        sev_class = "severity-low"
        if f.get("severity") == "Yüksek": sev_class = "severity-high"
        elif f.get("severity") == "Orta": sev_class = "severity-medium"

        findings_html += f"""
        <div class="finding">
            <h3>{f.get('title')}</h3>
            <p><strong>Risk Seviyesi:</strong> <span class="{sev_class}">{f.get('severity')}</span></p>
            <p><strong>Kategori:</strong> {f.get('category')}</p>
            <p><strong>Açıklama:</strong> {f.get('description')}</p>
            <table>
                <tr><th>Hedef / Etkilenen Bileşen</th><th>Detay</th></tr>
                <tr><td>{f.get('target')}</td><td><code>{f.get('detail')}</code></td></tr>
            </table>
        </div>
        """

    # HTML Şablonunu doldur
    final_html = HTML_TEMPLATE.format(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total=total,
        high=high,
        medium=medium,
        low=low,
        findings_html=findings_html
    )

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"[+] Başarılı! Rapor kaydedildi: {os.path.abspath(output_html)}")
    if os.name == 'nt':
        os.startfile(os.path.abspath(output_html))

def get_demo_findings():
    return [
        {
            "title": "Reflected Cross-Site Scripting (XSS)",
            "severity": "Yüksek",
            "category": "Web Exploitation",
            "target": "http://example.com/search?q=",
            "description": "Arama parametresinde kullanıcı girdisi filtrelenmeden ekrana basılıyor. Bu sayede tarayıcı üzerinde zararlı JavaScript kodları çalıştırılabilir.",
            "detail": "Payload: \"><script>alert(1)</script>"
        },
        {
            "title": "Time-Based Blind SQL Injection",
            "severity": "Yüksek",
            "category": "Web Exploitation",
            "target": "http://example.com/product.php?id=",
            "description": "Veritabanı sorgusu gecikmeli yanıt vererek SQL enjeksiyonuna olanak tanıyor.",
            "detail": "Payload: 1; WAITFOR DELAY '0:0:5'--"
        },
        {
            "title": "Zayıf Parola (FTP)",
            "severity": "Orta",
            "category": "Password Cracking",
            "target": "ftp://192.168.1.10",
            "description": "FTP servisine sözlük saldırısı ile başarılı bir şekilde giriş yapıldı.",
            "detail": "Kullanıcı: admin | Parola: password123"
        },
        {
            "title": "Açık Dizinler Bulundu",
            "severity": "Düşük",
            "category": "Web Exploitation",
            "target": "http://example.com/admin_backups/",
            "description": "Sunucu üzerinde gizli olması gereken yedekleme dizini keşfedildi.",
            "detail": "Durum Kodu: 200 OK"
        }
    ]

if __name__ == "__main__":
    generate_report("results.json")
