import os

from celery import shared_task
from asgiref.sync import async_to_sync
import aiogram


@shared_task
def send_new_order_notification(chat_id, message="Вам пришёл новый заказ!"):
    async def _async_send_new_order_notification():
        bot = aiogram.Bot(os.getenv("BOT_TOKEN"))
        await bot.send_message(chat_id, message)
    
    return async_to_sync(_async_send_new_order_notification)()
