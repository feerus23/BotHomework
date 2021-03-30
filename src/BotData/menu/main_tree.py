from vkbottle import BaseStateGroup, Keyboard, Text, BaseMiddleware
from vkbottle.bot import Blueprint, Message
from vkbottle_types.objects import UsersUserXtrCounters

from .. import data, keyboard

bp = Blueprint()

usr = {}

async def GetUInfo(user_id, fields=None, name_case=None):
    return (await bp.api.users.get(user_id, fields, name_case))[0]

async def resetData(id):
    del usr[id]
    await bp.state_dispenser.set(id, None)

class stateMenu(BaseStateGroup):
    #main_tree
    BEGIN = 0
    IGNORE = 1

    MAIN = 2
    
    #schedule_tree
    SCHEDULE = 3
    CWS = 4
    CLS = 5

    #admin_tree
    ADMIN_MAIN = 6

    ADMIN_UPD_1 = 7
    ADMIN_UPD_2 = 8

    ADMIN_SHW_1 = 9

    ADMIN_ADD_1 = 10
    ADMIN_ADD_2 = 11
    ADMIN_ADD_3 = 12

    #homework_tree
    HOMEWORK = 13
    CLS_HMWRK = 14
    OMPKS_HMW = 15

@bp.on.private_message(state=None)
async def begin_handler(message: Message):  
    usr.update([(message.peer_id, data.Users(message.peer_id))])

    info = await GetUInfo(message.from_id)
    if title := data.Title().Get(usr[message.peer_id].pGet(1)):
        msg = f'Рад вас видеть в добром здравии, товарищ {title}, {info.last_name}.'
    else:
        msg = 'Рад вас видеть в добром здравии, товарищ!'

    if usr[message.peer_id].pGet(0):
        await message.answer(msg, keyboard = keyboard.begin_menu())
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.BEGIN)
    else:
        await message.answer('Ты еще кто такой? Мне мама с незнакомцами запрещает разговаривать.')
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.IGNORE)
        return

@bp.on.private_message(state=stateMenu.BEGIN, payload={'cmd': 'main_menu'})
async def main_handler(message: Message):
    if data.isAdmin(usr[message.peer_id].pGet(1)):
        await message.answer('Чего изволите товарищ?', keyboard=keyboard.main_menu('admin'))
    else:
        await message.answer('Чего изволите товарищ?', keyboard=keyboard.main_menu())
    