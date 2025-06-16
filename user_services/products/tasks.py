import os

import requests
from celery import shared_task


@shared_task
def send_new_order_notification(chat_id, message="Вам пришёл новый заказ!"):
    token = os.getenv("BOT_TOKEN")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    requests.post(url, data={"chat_id": chat_id, "text": message}, timeout=7)
