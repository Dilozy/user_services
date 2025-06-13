from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.enums import ContentType
from aiogram.types import Message

import keyboards
from database.repository import UserTableRepository
from exceptions import DoesNotExist


router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    if await UserTableRepository.user_already_have(message.chat.id):
        await message.answer("Вы уже зарегистрированы в системе")
    else:
        await message.answer("Привет! Чтобы зарегистрировать тебя в системе," \
                             "мне нужен твой номер телефона.\n" \
                             "Чтобы отправить номер нажми на кнопку ниже.",
                             reply_markup=await keyboards.get_phone_markup())


@router.message(F.content_type == ContentType.CONTACT)
async def contact_handler(message: Message):
    phone_number = message.contact.phone_number
    chat_id = message.chat.id
    
    try:
        await UserTableRepository.update_chat_id(chat_id, phone_number)
        await message.answer("Вы успешно зарегистрированы в системе!")
    except DoesNotExist as err:
        await message.answer(str(err))
        