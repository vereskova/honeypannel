import requests
BOT_TOKEN = os.getenv("BOT_TOCKEN") 
CHAT_ID = os.getenv("CHAT_ID") 
def send_alert(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOCKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, json=payload)