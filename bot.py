# インストールした discord.py を読み込む
import random as ra
import re

import discord
#import chatbot

# 自分のBotのアクセストークンに置き換えてください.
TOKEN = 'NjMyMTAzODA2OTg5MTA3MjAx.Xahv4A.iDl1JTtxxJGWBKratbjh9fiBamk'

# 接続に必要なオブジェクトを生成
client = discord.Client()

def msg_neko():
    return "にゃーん"

def msg_kireji():
    reply = ""
    s = ["ブチ", "ぶち"][ra.randrange(2)]

    reply += s * ra.randrange(50)
    reply += "ィ" * ra.randrange(10)
    reply += "ッ" * ra.randrange(20)
    reply += "！" * ra.randrange(30)

    return reply

def msg_washlet():
    reply = ""
    reply += "ン゛" * ra.randrange(10)
    reply += "ッ" * ra.randrange(20)
    reply += "！" * ra.randrange(30)
    reply += ":rolling_eyes::anger:" * ra.randrange(30)

    return reply

def msg_unko():
    reply = ""
    s = ["ブリ", "モリ"][ra.randrange(2)]

    reply += s * ra.randrange(50)
    reply += "ィ" * ra.randrange(10)
    reply += "ッ" * ra.randrange(20)
    reply += "！" * ra.randrange(30)
    reply += "💩" * ra.randrange(30)

    return reply

def msg_omikuji():
    reply = ["大", "中", "小", "末", "凶", "大凶"][ra.randrange(6)]
    return reply + "便"

def msg_talk():
    pass


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

    # オウム返し
    for msg in message.content.split():
        if msg == '/neko':
            await message.channel.send(msg_neko())

        if msg == '/unko':
            await message.channel.send(msg_unko())

        if msg == '/kireji':
            await message.channel.send(msg_kireji())

        if msg == '/washlet':
            await message.channel.send(msg_washlet())

        if msg == '/omikuji':
            msg_ = msg_omikuji()
            await message.channel.send(msg_)

            if msg_ == "大便":
                await message.channel.send(msg_unko())

        if "[" in msg:
            await message.channel.send(msg.replace('[unko]', msg_unko()))

        if "💩" in msg:
            reply = ""
            reply += "ぶり" * [msg.count("💩")]
            reply += "っ"
            await message.channel.send(reply)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
