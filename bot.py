import os
import discord
from discord.ext import commands

# BotのAccess Token
# TOKEN = os.environ["TOKEN"]
TOKEN = "NjMyMTAzODA2OTg5MTA3MjAx.XcrPYQ.HcFzpPk2zxL7oGqbRRN3Af0n0NA"

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


# 起動
if __name__ == '__main__':
    bot = Bot(command_prefix='/')
    bot.run(TOKEN)
