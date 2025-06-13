from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton


async def get_phone_markup():
    builder = ReplyKeyboardBuilder()
    builder.add(
        KeyboardButton(
            text="Поделиться телефоном", 
            request_contact=True
        )
    )
    return builder.as_markup(resize_keyboard=True)