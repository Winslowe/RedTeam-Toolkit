#!/usr/bin/env python3
import json
import os
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def send_alert(message, title="🚨 ALERT"):
    config = load_config()
    if not config.get("notifications_enabled", False):
        return

    full_message = f"{title}\n\n{message}"
    
    # Telegram
    bot_token = config.get("telegram_bot_token", "")
    chat_id = config.get("telegram_chat_id", "")
    if bot_token and bot_token != "BURAYA_TOKEN_GIRILECEK" and chat_id and chat_id != "BURAYA_CHAT_ID_GIRILECEK":
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {"chat_id": chat_id, "text": full_message, "parse_mode": "HTML"}
        try:
            requests.post(url, json=data, timeout=5, verify=False)
        except:
            pass

    # Discord
    webhook = config.get("discord_webhook", "")
    if webhook and webhook != "BURAYA_WEBHOOK_URL_GIRILECEK":
        data = {"content": f"**{title}**\n```text\n{message}\n```"}
        try:
            requests.post(webhook, json=data, timeout=5, verify=False)
        except:
            pass

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        send_alert(" ".join(sys.argv[1:]), "🧪 TEST MESSAGE")
        print("[+] Test mesajı gönderildi (Eğer ayarlar doğruysa).")
    else:
        print("Kullanım: python Notifier.py 'Mesajınız'")
