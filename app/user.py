from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.database.requests import set_user
import app.keyboards as kb

user = Router()


@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id)
    await message.answer(
        "Для удаления нажми на задачу или напиши в чат новую",
        reply_markup=await kb.tasks(message.from_user.id),
    )
