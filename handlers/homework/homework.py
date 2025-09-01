import os
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from handlers.homework.utils import read_homework, write_homework

homework_router = Router()

HOMEWORK_FILE_PATH = os.path.join("files", "homework.txt")

class HomeworkStates(StatesGroup):
    waiting_for_homework_text = State()

@homework_router.message(F.text == "📚 Получить ДЗ")
async def get_homework(message: Message):
    homework_text = read_homework()
    await message.answer(f"ДЗ:\n{homework_text}")

@homework_router.message(F.text == "⬆️ Загрузить ДЗ")
async def upload_homework(message: Message, state: FSMContext):
    await message.answer("Отправь текст с новым ДЗ")
    await state.set_state(HomeworkStates.waiting_for_homework_text)

@homework_router.message(HomeworkStates.waiting_for_homework_text, F.text)
async def handle_homework_text(message: Message, state: FSMContext):
    new_homework = message.text.strip() #type: ignore
    write_homework(new_homework)
    await message.answer("✅ Домашнее задание успешно обновлено!")
    await state.clear() 

@homework_router.message(HomeworkStates.waiting_for_homework_text)
async def handle_wrong_input(message: Message):
    await message.answer("Пожалуйста, отправьте текст с новым ДЗ")