from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiohttp import web

from os import getenv

import ast

from dotenv import load_dotenv

load_dotenv()

ADMINS = ast.literal_eval(str(getenv("ADMINS", []))) # ? convert to list

def get_keyboard(user_id: int):
    buttons = [
        [KeyboardButton(text="📚 Получить ДЗ"), 
         KeyboardButton(text="📅 Получить расписание"), 
         KeyboardButton(text="🔔 Подписаться на рассылку")]
    ]
    if user_id in ADMINS:
        buttons.append(
            [KeyboardButton(text="⬆️ Загрузить ДЗ"), KeyboardButton(text="⬆️ Загрузить расписание")]
        )
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

async def handle_ping(request):
    return web.Response(text="Bot is alive!")

async def start_webserver():
    app = web.Application()
    app.add_routes([web.get("/", handle_ping)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    print("🌐 Web server started on port 8080")