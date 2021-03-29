import vkbottle
from vkbottle.bot import Bot, Message

import toml
import BotData

def main():
    bot = Bot(BotData.data.cfg['auth_data']['token'])

    for bp in BotData.bps:
        bp.load(bot)

    bot.run_forever()

if __name__ == '__main__':
    BotData.data.data.checkDatabase()
    main()