from vkbottle import BaseStateGroup, Keyboard, Text, BaseMiddleware, CtxStorage
from vkbottle.bot import Blueprint, Message
from vkbottle_types.objects import UsersUserXtrCounters
from . import data, kbrd

users = {}

bp = Blueprint()
some_db = CtxStorage()

class stateMenu(BaseStateGroup):
    IGNORE = 0
    MAIN = 1
    SCHEDULE = 2

async def GetUInfo(user_id):
    return (await bp.api.users.get(user_id))[0]

@bp.on.private_message(state=None)
async def begin_handler(message: Message):
    uid = message.peer_id
    
    users.update([(uid, data.Users(message.peer_id))])

    info = await GetUInfo(message.from_id)
    msg = f'Рад вас видеть в добром здравии, товарищ {data.Title().Get(users[uid].getParam(1))}, {info.last_name}.'

    if users[uid].getParam(0):
        await message.answer(msg, keyboard = kbrd.begin_menu())
        await bp.state_dispenser.set(uid, stateMenu.MAIN)
    else:
        await message.answer('Ты еще кто такой? Мне мама с незнакомцами запрещает разговаривать.')
        await bp.state_dispenser.set(uid, stateMenu.IGNORE)

@bp.on.private_message(state=stateMenu.MAIN, payload={'cmd': 'main_menu'})
async def main_handler(message: Message):
    await message.answer('Чего изволите товарищ?', keyboard=kbrd.main_menu())

@bp.on.private_message(state=stateMenu.MAIN, payload={'cmd': 'schedule_menu'})
async def schedule_handler(message: Message):
    #await bp.state_dispenser(message.peer_id, stateMenu.SCHEDULE)
    pass