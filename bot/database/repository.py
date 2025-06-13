from sqlalchemy import update, select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from .config import user_table, engine
from exceptions import DoesNotExist


class UserTableRepository:
    @staticmethod
    async def update_chat_id(chat_id, phone_number):
        async with AsyncSession(engine) as session:
            exists_stmt = select(
                    exists().where(user_table.c.phone.in_(
                        UserTableRepository.__normalize_phone(phone_number)
                        )
                    )
                )
            if not (await session.scalar(exists_stmt)):
                raise DoesNotExist(
                    "Пользователь с таким номером телефона не найден в системе"
                    )
        
            stmt = (
                update(user_table)
                .where(user_table.c.phone.in_(
                    UserTableRepository.__normalize_phone(phone_number))
                    )
                .values(telegram_chat_id=chat_id)
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def user_already_have(chat_id):
        async with AsyncSession(engine) as session:
            stmt = (
                select(
                    exists().where(user_table.c.telegram_chat_id == chat_id)
                )
            )

            result = await session.execute(stmt)
            return result.scalar()
        
    @staticmethod
    def __normalize_phone(phone_number):
        type1_phone_number = phone_number.replace(" ", "")
        type2_phone_number = phone_number.replace("+7", "8").replace(" ", "")
        return (type1_phone_number, type2_phone_number)