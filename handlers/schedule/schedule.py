import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from handlers.schedule.utils import get_schedule_image, save_schedule_image

schedule_router = Router()

class ScheduleStates(StatesGroup):
    waiting_for_schedule_img = State()

@schedule_router.message(F.text == "📅 Получить расписание")
async def get_schedule(message: Message):
    image_path = get_schedule_image()
    if image_path and os.path.exists(image_path):
        photo = FSInputFile(image_path)
        await message.answer_photo(photo, caption="📅 Ваше расписание:")
    else:
        await message.answer("Админы еще не загрузили расписание. Если эта ошибка повторяется, обратитесь к @Player_unknowner.")

@schedule_router.message(F.text == "⬆️ Загрузить расписание")
async def upload_schedule(message: Message, state: FSMContext):
    await message.answer("Отправьте изображение с расписанием")
    await state.set_state(ScheduleStates.waiting_for_schedule_img)

@schedule_router.message(ScheduleStates.waiting_for_schedule_img, F.photo)
async def handle_schedule_image(message: Message, state: FSMContext):
    try:
        photo = message.photo[-1] #type: ignore
        file_id = photo.file_id
        
        success = await save_schedule_image(message.bot, file_id) #type: ignore
        
        if success:
            await message.answer("✅ Расписание успешно обновлено!")
        else:
            await message.answer("❌ Произошла ошибка при сохранении расписания")
            
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")
    finally:
        await state.clear()

@schedule_router.message(ScheduleStates.waiting_for_schedule_img)
async def handle_wrong_input(message: Message):
    await message.answer("Пожалуйста, отправьте изображение с расписанием")