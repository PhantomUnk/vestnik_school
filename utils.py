from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_keyboard(user_id: int, ADMINS: list):
    buttons = [
        [KeyboardButton(text="📚 Получить ДЗ"), KeyboardButton(text="📅 Получить расписание")]
    ]
    if user_id in ADMINS:
        buttons.append(
            [KeyboardButton(text="⬆️ Загрузить ДЗ"), KeyboardButton(text="⬆️ Загрузить расписание")]
        )
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)