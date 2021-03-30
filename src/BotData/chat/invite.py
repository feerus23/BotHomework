from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.bot import FuncRule
from vkbottle.tools.dev_tools.mini_types.bot import MessageMin
from vkbottle_types.objects import MessagesMessageActionStatus

from ..data import cfg, saveCFG
from ..features import greeting

bp = Blueprint()

def has_bot_invited(message: MessageMin) -> bool:
    return (
        message.action
        and message.action.type == MessagesMessageActionStatus.CHAT_INVITE_USER
        and abs(message.action.member_id) == cfg['auth_data']['group_id']
    )


@bp.on.chat_message(FuncRule(has_bot_invited))
async def invite_mes_handler(message: MessageMin):
    await message.answer(greeting() + ''', товарищи, я коммунистический и хороший бот Дневничок. 
    Моё хобби - рассылать домашку пятиклассникам.
    И если вы хотите, чтобы я рассылал вам домашку, дорогие пятиклассники, дайте доступ ко всей беседе и админку.
    Спасибо за понимание.''')
