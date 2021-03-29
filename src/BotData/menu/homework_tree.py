from vkbottle.bot import Blueprint, Message
from vkbottle.exception_factory import VKAPIError

from .main_tree import stateMenu, usr, main_handler
from .. import data, keyboard

bp = Blueprint()

@bp.on.chat_message()
async def chat_message_handler(message: Message):
    await message.answer('Геометрия: -\nРусский:  21 вариант полностью и сочинение на листике\nФизика: -\n Физ-ра: -\nИнформатика: -')

@bp.on.private_message(payload={'cmd': 'undo_homework'})
async def homework_tree_undo_handler(message: Message):
    state = message.state_peer.state

    if state == stateMenu.SCHEDULE:
        await bp.state_dispenser.set(peer_id=message.peer_id, state=stateMenu.BEGIN, payload={'cmd': 'main_menu'})
        await main_handler(message)

@bp.on.private_message(state=stateMenu.BEGIN, payload = {'cmd': 'homework_menu'})
async def homework_handler(message: Message):
    await message.answer('Хорошо, выберите день недели или введите дату (в формате ГГГГ-ММ-ДД)', keyboard=keyboard.sedit_menu('homework_date_menu'))
    await bp.state_dispenser.set(peer_id=message.peer_id,state=stateMenu.HOMEWORK, payload = {'cmd': 'homework_date_menu'})

@bp.on.private_message(state=stateMenu.HOMEWORK, payload = {'cmd': 'homework_date_menu'})
async def homework_date_handler(message: Message):
    await message.answer('ТЕСТ')
    try:
        hmw = usr[message.peer_id].vSet(hobj=data.Homework(message.text))
    except ValueError:
        await message.answer('Вы ввели некорретные данные, попробуйте снова.')
        bp.state_dispenser.set(peer_id=message.peer_id,state=stateMenu.MAIN, payload = {'cmd': 'homework_menu'})
        await homework_handler(message)
    else:
        await message.answer(hmw.getHomework())
        pass