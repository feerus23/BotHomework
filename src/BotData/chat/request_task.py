from vkbottle.bot import Blueprint, Message
from datetime import date as Date

from ..data import Homework

bp = Blueprint()

@bp.on.chat_message(text = [ "/домашка", "/домашка <date>" ])
async def homework_sender_handler(message: Message, date: str = None):
    now = Date.today()

    if not date:
        await message.answer(Homework(now).getScheduleHomework())
    else:
        await message.answer(Homework(date).getScheduleHomework())