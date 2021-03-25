import vkbottle
from vkbottle.bot import Bot, Message

import toml
import BotData

cfg = toml.load('config.toml')
bot = Bot(cfg['auth_data']['token'])

for bp in BotData.bps:
    bp.load(bot)

bot.run_forever()