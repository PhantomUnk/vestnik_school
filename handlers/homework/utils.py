import os
from aiogram.types import Message
from handlers.broadcast.utils import get_broadcast_users

HOMEWORK_FILE_PATH = os.path.join("files", "homework.txt")

def ensure_files_directory():
    os.makedirs("files", exist_ok=True)

def read_homework():
    ensure_files_directory()
    try:
        with open(HOMEWORK_FILE_PATH, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        default_homework = "Что - то пошло не так. Напишите - @Player_unknowner"
        write_homework(default_homework)
        return default_homework

def write_homework(text):
    ensure_files_directory()
    with open(HOMEWORK_FILE_PATH, "w", encoding="utf-8") as file:
        file.write(text)

async def send_broadcast(message: Message, new_homework: str):
    if message.bot is None:
        return
    
    users = get_broadcast_users()
    
    formatted_homework = (
        "📢 <b>Какой - то Админ добавил ДЗ!</b>\n\n"
        f"{new_homework}\n\n"
    )

    for user_id in users:
        try:
            await message.bot.send_message(user_id, formatted_homework, parse_mode='HTML')
        except Exception as e:
            print(f"Error --- {e}")
