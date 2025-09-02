import os
import aiofiles
from aiogram import Bot

from aiogram.types import Message, FSInputFile
from handlers.broadcast.utils import get_broadcast_users

# ? Path to schedule image
SCHEDULE_IMAGE_PATH = os.path.join("files", "schedule.jpg")

def ensure_files_directory():
    os.makedirs("files", exist_ok=True)

def get_schedule_image():
    ensure_files_directory()
    
    if os.path.exists(SCHEDULE_IMAGE_PATH):
        return SCHEDULE_IMAGE_PATH
    return None

async def save_schedule_image(bot: Bot, file_id: str):
    try:
        ensure_files_directory()
        
        file = await bot.get_file(file_id)
        file_path = file.file_path
        
        if not file_path:
            return False
        
        downloaded_file = await bot.download_file(file_path)
        
        async with aiofiles.open(SCHEDULE_IMAGE_PATH, 'wb') as out_file:
            await out_file.write(downloaded_file.read()) #type: ignore
        
        return True
        
    except Exception as e:
        print(f"Error saving schedule image: {e}")
        return False
    
async def send_broadcast(message: Message):
    users = get_broadcast_users()

    if message.bot is None:
        return

    image_path = get_schedule_image()

    if not(image_path and os.path.exists(image_path)):
        return

    photo = FSInputFile(image_path) #type: ignore
    for user_id in users:
        try:
            await message.bot.send_photo(
                user_id,
                photo, 
                caption="📢 <b>Какой - то Админ добавил расписание!</b>\n\n", 
                parse_mode='HTML'
            )
        except Exception as e:
            print(f"Error --- {e}")