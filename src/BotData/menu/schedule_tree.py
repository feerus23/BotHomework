from vkbottle import BaseStateGroup, Keyboard, Text
from vkbottle.bot import Blueprint, Message


import re

from .main_tree import stateMenu, usr, main_handler
from .. import data, keyboard

bp = Blueprint()

SCHEDULE_STANDART = [ i for i in range(1,7) ]

@bp.on.private_message(payload={'cmd': 'undo_schedule'})
async def schedule_tree_undo_handler(message: Message):
    state = message.state_peer.state

    if state == stateMenu.CWS:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.SCHEDULE, payload={'cmd': 'sedit_menu'})
        await sedit_handler(message)
    elif state == stateMenu.CLS:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.CWS, payload={'cmd': 'cws_menu'})
        await cws_handler(message)    
    elif state == stateMenu.SCHEDULE:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.BEGIN, payload={'cmd': 'main_menu'})
        await main_handler(message)

'''@bp.on.private_message(state=stateMenu.BEGIN, payload={'cmd': 'schedule_menu'})
async def schedule_handler(message: Message):
    schedule = data.Schedule(SCHEDULE_STANDART)

    if schedule.isEmpty():
        await message.answer('Вау, еще ни одного урока в расписании не указано.')
        await message.answer('Хотите заполнить?', keyboard=keyboard.schedule_menu())
    else:
        await message.answer('Эм...))')
        await message.answer('Лол походу с чем-то напортачил...))', keyboard=keyboard.schedule_menu())    

    await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.MAIN)
'''

@bp.on.private_message(state=stateMenu.BEGIN, payload={'cmd': 'sedit_menu'})
async def sedit_handler(message: Message):
    await message.answer('Выберите день недели', keyboard=keyboard.sedit_menu())

    usr[message.peer_id].vDel('sobj')
    
    await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.SCHEDULE)

@bp.on.private_message(state=stateMenu.SCHEDULE, payload={'cmd': 'cws_menu'})
async def cws_handler(message: Message):
    schedule = usr[message.peer_id].vGet('sobj')

    if schedule is None:
        schedule = usr[message.peer_id].vSet(sobj=data.Schedule(message.text.capitalize()))

    tstr = schedule.getLesson()

    await message.answer(tstr)

    if schedule.compare():
        await message.answer('Выберите урок, который хотите изменить.', keyboard=keyboard.cls_menu(mode='apply'))
    else:
        await message.answer('Выберите урок, который хотите изменить.', keyboard=keyboard.cls_menu() if data.data.isAdmin(usr[message.peer_id].pGet(1)) else keyboard.undo_button('schedule'))

    await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.CWS)

@bp.on.private_message(state=stateMenu.CWS, payload={'cmd': 'apply_schedule'})
async def apply_schedule_handler(message: Message):
    schedule = usr[message.peer_id].vGet('sobj')

    await message.answer('Ваши изменения были сохранены')

    schedule.save()

    await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.MAIN, payload={'cmd': 'sedit_menu'})
    await sedit_handler(message)

@bp.on.private_message(state=stateMenu.CWS, payload={'cmd': 'cls_menu'})
async def cls_handler(message: Message):
    schedule = usr[message.peer_id].vGet('sobj')
    lesnum = usr[message.peer_id].vSet(lesnum=int(re.search(r'\d', message.text)[0]))

    await message.answer(f'Вы выбрали урок {schedule.getLesson(lessons_numbers = lesnum)}.\n Введите название урока на который хотите заменить этот урок.', keyboard=keyboard.undo_button('schedule'))

    if schedule.compare(lesson_numbers=lesnum):
        await message.answer(f'Также ваши не сохранённые изменения: {schedule.getLesson(lessons_numbers = lesnum, from_list=data.MODIFIED)}')
    
    await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.CLS)

@bp.on.private_message(state=stateMenu.CLS)
async def lesed_handler(message: Message):
    schedule = usr[message.peer_id].vGet('sobj')
    if message.text.lower() != 'назад':
        schedule.setLesson(schedule.getDow(2)[0], usr[message.peer_id].vGet('lesnum'), message.text)

        await message.answer('Успешно!')

        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.SCHEDULE, payload={'cmd': 'cws_menu'})
        await cws_handler(message)