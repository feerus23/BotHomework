from vkbottle import BaseStateGroup, Keyboard, Text, BaseMiddleware
from vkbottle.bot import Blueprint, Message
from vkbottle_types.objects import UsersUserXtrCounters

from .main_tree import stateMenu, usr, main_handler
from .. import data, keyboard

bp = Blueprint()

@bp.on.private_message(payload={'cmd': 'undo_admin'})
async def admin_tree_undo_handler(message: Message):
    state = message.state_peer.state

    if state == stateMenu.ADMIN_MAIN:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.BEGIN, payload={'cmd': 'main_menu'})
        await main_handler(message)
    elif state == stateMenu.ADMIN_UPD_1:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.BEGIN, payload={'cmd': 'admin_menu'})
        await amenu_handler(message)
    elif state == stateMenu.ADMIN_UPD_2:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.ADMIN_MAIN, payload={'cmd': 'al_upd_menu'})
        await al_upd_handler(message)
    elif state == stateMenu.ADMIN_SHW_1:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.BEGIN, payload={'cmd': 'admin_menu'})
        await amenu_handler(message)    

@bp.on.private_message(state=stateMenu.BEGIN, payload = {'cmd': 'admin_menu'})
async def amenu_handler(message: Message):
    await message.answer('Ну и ну вы разочаровываете партия', keyboard=keyboard.admin_menu())

    await bp.state_dispenser.set(message.peer_id, state=stateMenu.ADMIN_MAIN)

#INSERT-REPLACE BLOCK
@bp.on.private_message(state=stateMenu.ADMIN_MAIN, payload = {'cmd': 'al_upd_menu'})
async def al_upd_handler(message: Message):
    await message.answer('Введите номер уровня доступа', keyboard=keyboard.undo_button('admin'))
    await bp.state_dispenser.set(message.peer_id, state=stateMenu.ADMIN_UPD_1)
        
@bp.on.private_message(state=stateMenu.ADMIN_UPD_1)
async def alUpdInpNum_handler(message: Message):
    try:
        num = int(message.text)
    except ValueError:
        await message.answer('Введите корректный номер!', keyboard=keyboard.undo_button('admin'))
        await bp.state_dispenser.set(message.peer_id, state=stateMenu.ADMIN_UPD_1)
    else:
        usr[message.peer_id].vSet(level_number=num)

        await message.answer('Хорошо! Теперь введите название к этому уровню доступа! Отправьте 0, если хотите удалить', keyboard=keyboard.undo_button('admin'))
        await bp.state_dispenser.set(message.peer_id, state=stateMenu.ADMIN_UPD_2)

@bp.on.private_message(state=stateMenu.ADMIN_UPD_2)
async def alUpdInpName_handler(message: Message):
    lvl_num = usr[message.peer_id].vGet('level_number')

    if message.text == '0':
        data.Title().Del(lvl_num)
    else:
        data.Title().Set(**{ str(lvl_num): message.text })

    await message.answer('Успешно!')
    
    await bp.state_dispenser.set(message.peer_id, state=stateMenu.BEGIN, payload={'cmd': 'admin_menu'})
    await amenu_handler(message)

#SHOW BLOCK
@bp.on.private_message(state=stateMenu.ADMIN_MAIN, payload = {'cmd': 'al_shw_menu'})
async def al_shw_handler(message: Message):
    string = str()

    if titles := data.Title().GetAll():
        for title in titles:
            string += f'{title[0]} - {title[1]}'
            if titles.index(title) != len(titles) - 1:
                string += '\n'
    else:
        string = 'Еще ни одного уровня нет'
    
    await message.answer(string, keyboard=keyboard.undo_button('admin'))
    await bp.state_dispenser.set(message.peer_id, stateMenu.ADMIN_SHW_1)

