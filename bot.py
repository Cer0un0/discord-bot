# インストールした discord.py を読み込む
import discord
import random as ra
import re

# 自分のBotのアクセストークンに置き換えてください
# a
TOKEN = 'NjMyMTAzODA2OTg5MTA3MjAx.XaGuag.FDCTiWyycPKxYq-jgWRrF0W-RcY'

# 接続に必要なオブジェクトを生成
client = discord.Client()

def char_unko():
    reply = ""
    s = ["ブリ", "モリ"][ra.randrange(2)]
    for i in range(ra.randrange(50)):
        reply += s
    for i in range(ra.randrange(10)):
        reply += "ィ"
    for i in range(ra.randrange(20)):
        reply += "ッ"
    for i in range(ra.randrange(30)):
        reply += "！"
    for i in range(ra.randrange(20)):
        reply += "💩"

    return reply


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if re.match('(\d+)d(\d+)', message.content):
        n, me = map(int, message.content.split("d"))
        reply = ""
        for i in range(n):
            reply += f"{ra.randrange(me)+1} "

        await message.channel.send(reply)
        return

    for msg in message.content.split():
        # 「/neko」と発言したら「にゃーん」が返る処理
        if msg == '/neko':
            await message.channel.send('にゃーん')
            continue

        if msg == '/unko':
            await message.channel.send(char_unko())
            continue

        if "[" in msg:
            await message.channel.send(msg.replace('[unko]', char_unko()))

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
