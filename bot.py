# インストールした discord.py を読み込む
import random as ra
import re
import sys

import discord

# 自分のBotのアクセストークンに置き換えてください.
TOKEN = 'NjMyMTAzODA2OTg5MTA3MjAx.Xa2-GA.5fmJoCILrpkylFoiCg4HmsNalj4'

dict_repetition = {
    "/unko": [["ぶり", "もり", "ぶぴ", "べちょ", "もぐ", "みち"], "ッ", "！", "💩"],
    "/kireji": [["ぶち", "ブチ"], "ィ", "ッ", "！", "💉"],
    "/washlet": ["ン゛", "ッ", "！", "🙄💢"]
}

# 接続に必要なオブジェクトを生成
client = discord.Client()

def msg_neko():
    return "にゃーん"

#
def msg_repetition(qu):
    reply = ""
    for rep in dict_repetition[qu]:
        if type(rep) is str:
            reply += rep * ra.randrange(40)
        else:
            reply += rep[ra.randrange(len(rep))] * ra.randrange(60)

    return reply

def msg_omikuji():
    reply = ["大", "中", "小", "末", "凶", "大凶"][ra.randrange(6)]
    return reply + "便"

def msg_slot_hamako():
    reply = ""
    reply += ["ハ", "ヒ", "フ", "へ", "ホ"][ra.randrange(5)]
    reply += ["マ", "ミ", "ム", "メ", "モ"][ra.randrange(5)]
    reply += ["カ", "キ", "ク", "ケ", "コ"][ra.randrange(5)]

    return reply + "ー"

def msg_slot_daikon():
    reply = ""
    reply += ["カラー", "ダイ"][ra.randrange(2)]
    reply += ["コーン", "コン"][ra.randrange(2)]

    return reply

def msg_slot_zero():
    reply = ""
    reply += ["ぜろ", "いち"][ra.randrange(2)]
    reply += ["ホモ", "レズ", "バイ", "ゲイ"][ra.randrange(4)]

    return reply

def msg_slot_aratan():
    reply = ""
    reply += ["あら"][ra.randrange(1)]
    reply += ["たん", "たそ", "た", "くん", "ちゃん"][ra.randrange(5)]

    return reply

def msg_slot_unbobo():
    reply = ""
    reply += ["うん"][ra.randrange(1)]
    reply += ["ば", "び", "ぶ", "べ", "ぼ"][ra.randrange(5)]
    reply += ["ば", "び", "ぶ", "べ", "ぼ"][ra.randrange(5)]

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
    for qu in message.content.split():
        await message.channel.send(message.content.split())
        await message.channel.send(qu in dict_repetition.keys())
        continue

        if qu == '/neko':
            await message.channel.send(msg_neko())

        if qu in dict_repetition.keys():
            await message.channel.send(msg_repetition(qu))

        if qu == '/omikuji':
            msg_ = msg_omikuji()
            await message.channel.send(msg_)

            if msg_ == "大便":
                await message.channel.send(msg_unko())

        if qu == '/slot':
            r = ra.randrange(5)
            if r == 0:
                msg_ = msg_slot_hamako()
            if r == 1:
                msg_ = msg_slot_daikon()
            if r == 2:
                msg_ = msg_slot_zero()
            if r == 3:
                msg_ = msg_slot_aratan()
            if r == 4:
                msg_ = msg_slot_unbobo()

            await message.channel.send(msg_)

            if msg_ == "ハマコー" or msg_ == "ダイコン" or msg_ == "ぜろホモ" or msg_ == "あらたん" or msg_ == "うんぼぼ":
                await message.channel.send(msg_unko())

        if qu == '/ochinpo':
            str = ['お', 'ち', 'ん', 'ぽ']
            complete = 0
            cnt = 0
            rnd = 0
            msg_ = ""
            while complete < 4:
                cnt += 1
                rnd = ra.randint(0, 3)
                msg_ += str[rnd]
                complete = complete+1 if rnd == complete else 0
            await message.channel.send(msg_)
            await message.channel.send(f"おぉぉおﾞおﾞ～っ！！イグゥウ！！イッグゥウウ！！{cnt}回目で果てました...")

        # if message.content.startswith('/ommc'):
        #    channel = client.get_channel('nyr')
        #
        #    if client.is_voice_connected(channel.server):
        #        voice = client.voice_client_in(channel.server)
        #    else:
        #        voice = await client.join_voice_channel(channel)
        #
        #     #mp3ファイルはこのプログラムと同じ階層の場所に入れること.
        #     player = voice.create_ffmpeg_player('ommc.mp3')
        #     player.start()

        if "[" in msg:
            await message.channel.send(msg.replace('[unko]', msg_unko()))

        # if ":poop" in msg:
        #     reply = ""
        #     reply += "ぶり" * [msg.count(":poop")]
        #     reply += "っ"
        #     await message.channel.send(reply)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
