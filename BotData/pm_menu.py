from vkbottle import BaseStateGroup, Keyboard, Text, BaseMiddleware
from vkbottle.bot import Blueprint, Message
from vkbottle_types.objects import UsersUserXtrCounters

import re

from . import data, kbrd

usr = {}

bp = Blueprint()

SCHEDULE_STANDART = [ i for i in range(1,7) ]

class stateMenu(BaseStateGroup):
    BEGIN = 0
    IGNORE = 1
    MAIN = 2
    SCHEDULE = 3
    CWS = 4
    CLS = 5

async def GetUInfo(user_id):
    return (await bp.api.users.get(user_id))[0]

async def resetData(id):
    del usr[id]
    await bp.state_dispenser.set(id, None)

@bp.on.private_message(payload={'cmd': 'undo'})
async def undo_handler(message: Message):
    state = message.state_peer.state

    if state == stateMenu.MAIN:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.BEGIN, payload={'cmd': 'main_menu'})
        await main_handler(message)
    elif state == stateMenu.SCHEDULE:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.BEGIN, payload={'cmd': 'main_menu'})
        await main_handler(message)
    elif state == stateMenu.CWS:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.SCHEDULE, payload={'cmd': 'cws_menu'})
        await cws_handler(message)
    elif state == stateMenu.CLS:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.CWS, payload={'cmd': 'cls_menu'})
        await cls_handler(message)

@bp.on.private_message(state=None)
async def begin_handler(message: Message):  
    usr.update([(message.peer_id, data.Users(message.peer_id))])

    info = await GetUInfo(message.from_id)
    msg = f'Рад вас видеть в добром здравии, товарищ {data.Title().Get(usr[message.peer_id].getParam(1))}, {info.last_name}.'

    if usr[message.peer_id].getParam(0):
        await message.answer(msg, keyboard = kbrd.begin_menu())
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.BEGIN)
    else:
        await message.answer('Ты еще кто такой? Мне мама с незнакомцами запрещает разговаривать.')
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.IGNORE)
        return

@bp.on.private_message(state=stateMenu.BEGIN, payload={'cmd': 'main_menu'})
async def main_handler(message: Message):
    await message.answer('Чего изволите товарищ?', keyboard=kbrd.main_menu())
    

'''@bp.on.private_message(state=stateMenu.BEGIN, payload={'cmd': 'schedule_menu'})
async def schedule_handler(message: Message):
    schedule = data.Schedule(SCHEDULE_STANDART)

    if schedule.isEmpty():
        await message.answer('Вау, еще ни одного урока в расписании не указано.')
        await message.answer('Хотите заполнить?', keyboard=kbrd.schedule_menu())
    else:
        await message.answer('Эм...))')
        await message.answer('Лол походу с чем-то напортачил...))', keyboard=kbrd.schedule_menu())    

    await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.MAIN)
'''

@bp.on.private_message(state=stateMenu.BEGIN, payload={'cmd': 'sedit_menu'})
async def sedit_handler(message: Message):
    await message.answer('Выберите день недели', keyboard=kbrd.sedit_menu())

    if usr[message.peer_id].vGet('sobj'):
        usr[message.peer_id].vDel('sobj')
    
    await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.SCHEDULE)

@bp.on.private_message(state=stateMenu.SCHEDULE, payload={'cmd': 'cws_menu'})
async def cws_handler(message: Message):
    schedule = usr[message.peer_id].vGet('sobj')

    if schedule is None:
        schedule = usr[message.peer_id].vSet(sobj=data.Schedule(message.text.capitalize()))

    tstr = schedule.getLesson()

    await message.answer(tstr)

    #await message.answer(schedule.getRes(data.MODIFIED))
    if schedule.compare():
        await message.answer('Выберите урок, который хотите изменить.', keyboard=kbrd.cls_menu_apply())
    else:
        await message.answer('Выберите урок, который хотите изменить.', keyboard=kbrd.cls_menu())

    await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.CWS)

@bp.on.private_message(state=stateMenu.CWS, payload={'cmd': 'apply'})
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

    await message.answer(f'Вы выбрали урок {schedule.getLesson(lessons_numbers = lesnum)}.\n Введите название урока на который хотите заменить этот урок.', keyboard=kbrd.undo_button())

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