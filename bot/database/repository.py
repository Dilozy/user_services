from sqlalchemy import update, select, exists

from .config import user_table, engine


class UserTableRepository:
    @staticmethod
    def update_chat_id(chat_id, phone_number):
        stmt = (
            update(user_table)
            .where(user_table.c.phone.in_(
                UserTableRepository.__normalize_phone(phone_number))
                )
            .values(telegram_chat_id=chat_id)
        )

        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def user_already_have(chat_id):
        stmt = (
            select(
                exists().where(user_table.c.telegram_chat_id == chat_id)
            )
        )

        with engine.connect() as conn:
            result = conn.execute(stmt)
            return result.scalar()
        
    @staticmethod
    def __normalize_phone(phone_number):
        type1_phone_number = phone_number.replace(" ", "")
        type2_phone_number = phone_number.replace("+7", "8").replace(" ", "")
        return (type1_phone_number, type2_phone_number)