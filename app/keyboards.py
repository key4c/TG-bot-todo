from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.database.requests import get_tasks


async def tasks(tg_id):
    tasks = await get_tasks(tg_id)
    keybord = InlineKeyboardBuilder
    for task in tasks:
        keybord.add(
            InlineKeyboardButton(text=task.task, callback_dta=f"task_{task.id}")
        )
        return keybord
