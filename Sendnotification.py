import requests
import json
import os

def send_telegram_notification(message_text):

    with open('config.json', 'r') as f:
        config = json.load(f)
    bot_token = os.getenv("TELEGRAM_API_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    

    params = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "Markdown" 
    }
    
    try:

        response = requests.post(url, params=params)
        response.raise_for_status()
        print("Notification sent successfully!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    notification_message = "Hello from your Python script! This is a **notification** with *Markdown* formatting and a [link to the docs](core.telegram.org)."

    send_telegram_notification(notification_message)
