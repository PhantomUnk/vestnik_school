from aiogram import Router, F
from aiogram.types import Message

from handlers.broadcast.utils import add_user

broadcast_router = Router()

@broadcast_router.message(F.text == "🔔 Подписаться на рассылку")
async def subscribe_broadcast(message: Message):
    success = add_user(message.from_user.id)  #type: ignore
    if success:
        await message.answer(
            "✅ Вы успешно подписались на рассылку! " \
            "Теперь вы будете получать новые ДЗ автоматически."
        )
    else:
        await message.answer(
            "❌ Вы отписались от рассылки.\n"
            "Больше новые ДЗ приходить не будут."
        )
