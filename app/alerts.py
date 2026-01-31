import os 
import requests


BOT_TOKEN = os.getenv("BOT_TOKEN") 
CHAT_ID = os.getenv("CHAT_ID") 
def send_alert(message: str):
    if not BOT_TOKEN or not CHAT_ID:
        print(" Telegram env vars not set", BOT_TOKEN, CHAT_ID)
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        r = requests.post(url, json=payload, timeout=10)
        print("TG RESPONSE:", r.status_code, r.text)
    except Exception as e:
        print("TG EXCEPTION:", e)
