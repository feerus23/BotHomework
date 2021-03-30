from vkbottle.bot import Blueprint, Message
from vkbottle.exception_factory import VKAPIError

import re

from .main_tree import stateMenu, usr, main_handler
from .. import data, keyboard

bp = Blueprint()

@bp.on.private_message(payload={'cmd': 'undo_homework'})
async def homework_tree_undo_handler(message: Message):
    state = message.state_peer.state

    if state == stateMenu.HOMEWORK:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.BEGIN, payload={'cmd': 'main_menu'})
        await main_handler(message)
    elif state == stateMenu.CLS_HMWRK:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.HOMEWORK, payload={'cmd': 'homework_menu'})
        await homework_handler(message)

@bp.on.private_message(state=stateMenu.BEGIN, payload = {'cmd': 'homework_menu'})
async def homework_handler(message: Message):
    await message.answer('Хорошо, выберите день недели или введите дату (в формате ГГГГ-ММ-ДД)', keyboard=keyboard.sedit_menu('homework'))
    await bp.state_dispenser.set(peer_id=message.peer_id,state=stateMenu.HOMEWORK)

@bp.on.private_message(state=stateMenu.HOMEWORK)
async def homework_date_handler(message: Message):
    try:
        hmw = usr[message.peer_id].vSet(hobj=data.Homework(message.text))
    except ValueError:
        await message.answer('Вы ввели некорретные данные, попробуйте снова.')
        await bp.state_dispenser.set(peer_id=message.peer_id,state=stateMenu.MAIN, payload = {'cmd': 'homework_menu'})
        await homework_handler(message)
    else:
        usr[message.peer_id].vSet(dow=hmw.getWeekday())
        await message.answer(hmw.getScheduleHomework(), keyboard = keyboard.cls_menu('homework') if data.data.isAdmin(usr[message.peer_id].pGet(1)) else keyboard.undo_button('homework'))
        await bp.state_dispenser.set(peer_id=message.peer_id,state=stateMenu.CLS_HMWRK, payload = {'cmd': 'hmw_cls_menu'})

@bp.on.private_message(state=stateMenu.CLS_HMWRK, payload = {'cmd': 'hmw_cls_menu'})
async def cls_homework_handler(message: Message):
    lesson_number = int(re.search(r'\d+', message.text)[0])
    hobj = usr[message.peer_id].vGet('hobj')

    lesson = data.Schedule(hobj.getWeekday()).getLesson(lessons_numbers = lesson_number)

    await message.answer(f'Вы выбрали урок {lesson}.\n Задайте домашнее задание к этому уроку.', keyboard=keyboard.undo_button('homework'))
    await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.OMPKS_HMW)

@bp.on.private_message(state=stateMenu.OMPKS_HMW)
async def ompks_hmw_handler(message: Message):
    