import requests
import json
import os

def send_telegram_notification(message_text):

    with open('config.json', 'r') as f:
        config = json.load(f)

    url = f"https://api.telegram.org/bot{config['BOT_TOKEN']}/sendMessage"
    

    params = {
        "chat_id": config['CHAT_ID'],
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