# インストールした discord.py を読み込む
import discord
import random as ra

# 自分のBotのアクセストークンに置き換えてください
# a
TOKEN = 'NjMyMTAzODA2OTg5MTA3MjAx.XaBBQg.nle5WkuPvYSo1EB6aaviB7CbU70'

# 接続に必要なオブジェクトを生成
client = discord.Client()



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

    await message.channel.send(message.content)

    for msg in message.content.split():
        # 「/neko」と発言したら「にゃーん」が返る処理
        if msg == '/neko':
            await message.channel.send('にゃーん')

        if msg == '/unko':
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
            await message.channel.send(reply)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
