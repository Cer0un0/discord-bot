# TODO: Help
# regist contest

###
# ライブラリ
###
import random as ra
import re
import sys

import discord

###
# 定義
###

# BotのAccess Token
TOKEN = 'NjMyMTAzODA2OTg5MTA3MjAx.Xa34lA.Et8qCwcgqhsPGIUryBck-Fj_d4Q'

# 1回応答するだけの単語辞書
dict_response = {
    "/neko"      : "にゃーん"
    # "/colorcorn" : ":colorcorn:"
}
# ランダムで繰り返す単語辞書
dict_repetition = {
    "/kireji"  : [["ぶち", "ブチ"], "ィ", "ッ", "！", "💉"],
    "/shikko"  : [["ちょろ", "チョロ"], "💦"],
    "/unbobo"  : [["うんぼぼうんぼぼウッホッホ！！！！"], "💩"],
    "/unko"    : [["ぶり", "もり", "ぶぴ", "べちょ", "もぐ", "みち"], "ッ", "！", "💩"],
    "/washlet" : [["ン゛"], "ッ", "！", "🙄💢"]
}
# スロットの単語辞書
#   word: どれか1要素が選ばれる
#           0番目は末尾に付ける単語
#   atari: key -> 当たりの単語,
#          value -> 当たったときの文
#                   クエリが存在すれば実行
#                   ""でクエリをランダムで実行
dict_slot = {
    "/aratan"  : {
        "word"   : ["", ["あら"], ["たん", "たそ", "くん", "ちゃん", "たそくんちゃん先輩"]],
        "atari"  : {
            "あらたん"   : ""
        }
    },
    "/daikon"  : {
        "word"   : ["", ["ダイ", "カラー"], ["コン", "コーン"]],
        "atari"  : {
            "ダイコン"   : ""
            # "カラーコーン": "/colorcorn"
        }
    },
    "/hamako"  : {
        "word"   : ["ー", ["ハ", "ヒ", "フ", "ヘ", "ホ"], ["マ", "ミ", "ム", "メ", "モ"], ["カ", "キ", "ク", "ケ", "コ"]],
        "atari"  : {
            "ハマコー"   : ""
        }
    },
    "/omikuji" : {
        "word"   : ["便", ["大", "中", "吉", "小", "末", "凶", "大凶"]],
        "atari"  : {
            "大便"      : "/unko",
            "小便"      : "/shikko"
        }
    },
    "/satori"  : {
        "word"   : ["", ["うん"], ["ば", "び", "ぶ", "べ", "ぼ"], ["ば", "び", "ぶ", "べ", "ぼ"]],
        "atari"  : {
            "うんぼぼ"   : "/unbobo"
        }
    },
    "/zero"  : {
        "word"   : ["", ["ぜろ", "いち"], ["ホモ", "レズ", "ゲイ", "バイ"]],
        "atari"  : {
            "ぜろホモ"   : ""
        }
    }
}

mslot_list = ["/aratan", "/daikon", "/hamako", "/satori", "/zero"]

###
# 以下処理
###

# 接続に必要なオブジェクトを生成
client = discord.Client()

def msg_response(qu):
    """
    クエリに対応する、1回応答するだけのメッセージ

    ----------
    qu: sting
        メッセージ呼び出しコマンド（dict_response.key）
    """

    return dict_response[qu]

def msg_repetition(qu):
    """
    クエリに対応する、リスト内の単語をランダムで繰り返すメッセージ

    ----------
    qu: sting
        メッセージ呼び出しコマンド（dict_repetition.key）
    """

    reply = ""
    for rep in dict_repetition[qu]:
        if type(rep) is str: # string
            reply += rep * ra.randrange(40)
        else: # list
            reply += ra.choice(rep) * ra.randrange(60)

    return reply

def msg_slot(qu):
    """
    クエリに対応する、スロット結果のメッセージ

    ----------
    qu: sting
        メッセージ呼び出しコマンド（dict_slot.key）
    """

    reply = ""
    # dict_slotに基づいて単語生成
    for li in dict_slot[qu]["word"][1:]:
        reply += ra.choice(li)

    # 末尾の単語を付ける
    return reply + dict_slot[qu]["word"][0]

def msg_dice(qu, pattern):
    """
    ダイス

    ----------
    qu: sting
        ダイス結果メッセージ
    """

    n, me = map(int, re.match(pattern, qu).group(1))
    reply = ""
    for i in range(n):
        reply += f"{ra.randrange(me) + 1}"

    # re.split('\d+', s_nums)

    return qu
#
#
async def do_slot(qu, message):
    """
    クエリに対応する、スロットを実行

    ----------
    qu: sting
        メッセージ呼び出しコマンド（dict_slot.key）
    """

    # '/slot'の場合、ランダムにクエリを選択
    if qu == '/slot':
        qu = ra.choice(list(dict_slot.keys()))

    # 結果の投稿
    result = msg_slot(qu)
    await message.channel.send(result)

    # 当たりの処理結果を投稿
    if result in dict_slot[qu]["atari"].keys():
        qu_ = dict_slot[qu]["atari"][result]

        if qu_ == "":  # ランダムでクエリを実行
            qu_ = ra.choice(list(dict_repetition.keys()))
            await message.channel.send(msg_repetition(qu_))
        else:
            if qu_ in dict_response:  # 1つだけ応答の存在判定
                await message.channel.send(msg_response(qu_))
            if qu_ in dict_repetition:  # 繰り返し応答の存在判定
                await message.channel.send(msg_repetition(qu_))


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    # 1行ずつ処理
    for qu in message.content.split():
        # 1回だけの応答用
        if qu in dict_response.keys():
            await message.channel.send(msg_response(qu))

        # 繰り返しの単語用
        if qu in dict_repetition.keys():
            await message.channel.send(msg_repetition(qu))

        # スロット
        if qu in dict_slot.keys() or qu == '/slot':
            await do_slot(qu, message)

        # ダイス
        PATTERN = '(\d+)d(\d+)'
        await message.channel.send(re.match(PATTERN, qu))
        if re.match(PATTERN, qu):
            await message.channel.send(msg_dice(qu, PATTERN))

        # おちんぽプログラム
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

        if "[" in qu:
            await message.channel.send(qu.replace('[unko]', msg_repetition("/unko")))


        # if ":poop" in msg:
        #     reply = ""
        #     reply += "ぶり" * [msg.count(":poop")]
        #     reply += "っ"
        #     await message.channel.send(reply)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
