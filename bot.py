import asyncio
import time
from datetime import datetime, timedelta, timezone
import os

import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep

# BotのAccess Token
TOKEN = os.environ["TOKEN"]

# 読み込むコグの名前を格納しておく。
INITIAL_EXTENSIONS = [
    'cogs.cog'
]


# クラスの定義。ClientのサブクラスであるBotクラスを継承。
class Bot(commands.Bot):
    # MyBotのコンストラクタ。
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

        self.remove_command('help')

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        for cog in INITIAL_EXTENSIONS:
            self.load_extension(cog)

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        channel = self.get_channel(int(os.environ["CHANNEL_DEVROOM"]))
        await channel.send("アップデートを反映しました")

        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')

        # VC 通知
        # while True:
        #     time_ = datetime.now(timezone(timedelta(hours=+9), 'JST'))
        #     has_vcdata = False
        #
        #     if has_vcdata:
        #         pass
        #     else:
        #         print("a")
        #         scope = ['https://spreadsheets.google.com/feeds',
        #                  'https://www.googleapis.com/auth/drive']
        #
        #         credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread.json', scope)
        #         gc = gspread.authorize(credentials)
        #         worksheet = gc.open('DiscordBot').worksheet('virtual-contest')
        #
        #         title = worksheet.acell('A1').value
        #         t_start = worksheet.acell('B1').value
        #         t_end = worksheet.acell('C1').value
        #         link = worksheet.acell('D1').value
        #
        #         has_vcdata = True
        #
        #     if time_.strftime("%Y-%m-%d %H:%M") == f"{t_start}":
        #         await channel.send(f"【{title}】始まりました\n{link}")
        #
        #     # await channel.send(time_.strftime("%Y/%m/%d %H:%M"))
        #     # if time_.strftime("%Y-%m-%d %H:%M") == f"{t_start[:-1]}{t_start[-1]-1 }":
        #     await asyncio.sleep(1)
        #     # else:
        #     #     await asyncio.sleep(30)


# 起動
if __name__ == '__main__':
    bot = Bot(command_prefix='/')
    bot.run(TOKEN)
