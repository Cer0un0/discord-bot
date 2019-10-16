# インストールした discord.py を読み込む
import random as ra
import re

import discord
import chatbot

# 自分のBotのアクセストークンに置き換えてください.
TOKEN = 'NjMyMTAzODA2OTg5MTA3MjAx.XaeoUw.ukx3wtlXE_dtZ2a90xoI56xRXTA'

# 接続に必要なオブジェクトを生成
client = discord.Client()

def msg_neko():
    return "にゃーん"

def msg_unko():
    reply = ""
    s = ["ブリ", "モリ"][ra.randrange(2)]

    reply += s * ra.randrange(50)
    reply += "ィ" * ra.randrange(10)
    reply += "ッ" * ra.randrange(20)
    reply += "！" * ra.randrange(30)
    reply += "💩" * ra.randrange(30)

    return reply

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
            continue
        elif msg == '/unko':
            await message.channel.send(msg_unko())
            continue
        elif "[" in msg:
            await message.channel.send(msg.replace('[unko]', char_unko()))
            continue
        else:
            reply = ""
            reply += "ぶり" * [msg.count("💩")]
            await message.channel.send(reply + "っ")

        msg_talk()

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
