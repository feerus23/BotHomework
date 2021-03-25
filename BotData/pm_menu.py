from vkbottle import BaseStateGroup, Keyboard, Text, BaseMiddleware, CtxStorage
from vkbottle.bot import Blueprint, Message
from vkbottle_types.objects import UsersUserXtrCounters

import re

from . import data, kbrd

users = {}

bp = Blueprint()
tdb = CtxStorage()

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
    del users[id]
    await bp.state_dispenser.set(id, None)


@bp.on.private_message(state=None)
async def begin_handler(message: Message):  
    users.update([(message.peer_id, data.Users(message.peer_id))])

    info = await GetUInfo(message.from_id)
    msg = f'Рад вас видеть в добром здравии, товарищ {data.Title().Get(users[message.peer_id].getParam(1))}, {info.last_name}.'

    if users[message.peer_id].getParam(0):
        await message.answer(msg, keyboard = kbrd.begin_menu())
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.BEGIN)
    else:
        await message.answer('Ты еще кто такой? Мне мама с незнакомцами запрещает разговаривать.')
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.IGNORE)
        return

@bp.on.private_message(state=stateMenu.BEGIN, payload={'cmd': 'main_menu'})
async def main_handler(message: Message):
    await message.answer('Чего изволите товарищ?', keyboard=kbrd.main_menu())
    

@bp.on.private_message(state=stateMenu.BEGIN, payload={'cmd': 'schedule_menu'})
async def schedule_handler(message: Message):
    schedule = data.Schedule(SCHEDULE_STANDART).getRes()

    if len(schedule) == 0:
        await message.answer('Вау, еще ни одного урока в расписании не указано.')
        await message.answer('Хотите заполнить?', keyboard=kbrd.schedule_menu())

    await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.MAIN)

@bp.on.private_message(state=stateMenu.MAIN, payload={'cmd': 'sedit_menu'})
async def sedit_handler(message: Message):
    await message.answer('Выберите день недели', keyboard=kbrd.sedit_menu())
    await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.SCHEDULE)

@bp.on.private_message(state=stateMenu.SCHEDULE, payload={'cmd': 'cws_menu'})
async def cws_handler(message: Message):
    tstr = ''

    schedule = tdb.get(message.peer_id)
    if schedule is None:
        tdb.set(message.peer_id, data.Schedule(message.text.lower()))
        schedule = tdb.get(message.peer_id)

    await message.answer(message.text)
    for les in schedule.getLesson(SCHEDULE_STANDART):
        tstr += les + '\n'

    await message.answer(tstr)

    if schedule.compare():
        await message.answer('Выберите урок, который хотите изменить.', keyboard=kbrd.cls_menu_apply())
    else:
        await message.answer('Выберите урок, который хотите изменить.', keyboard=kbrd.cls_menu())

    await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.CWS)

@bp.on.private_message(state=stateMenu.CWS, payload={'cmd': 'cls_menu'})
async def cls_handler(message: Message):
    schedule = tdb.get(message.peer_id)
    lesnum = int(re.search(r'\d', message.text)[0])

    await message.answer(f'Вы выбрали урок {schedule.getLesson(lesnum)[0]}.\n Введите название урока на который хотите заменить этот урок.')

    if schedule.compare():
        await message.andwer(f'Также ваши не сохранённые изменения: {lesnum}')
    
    await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.CLS)


@bp.on.private_message(payload={'cmd': 'undo'})
async def undo_handler(message: Message):
    state = message.state_peer.state

    if state == stateMenu.MAIN:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.BEGIN, payload={'cmd': 'main_menu'})
        await main_handler(message)
    elif state == stateMenu.SCHEDULE:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.BEGIN, payload={'cmd': 'schedule_menu'})
        await schedule_handler(message)
    elif state == stateMenu.CWS:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.MAIN, payload={'cmd': 'sedit_menu'})
        await sedit_handler(message)
    elif state == stateMenu.CLS:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.SCHEDULE, payload={'cmd': 'cws_menu'})
        await cws_handler(message)