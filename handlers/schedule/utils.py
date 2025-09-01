import os
import aiofiles
from aiogram import Bot

# Путь к файлу расписания
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