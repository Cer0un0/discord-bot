# TODO: Help
# unbobo

###
# ライブラリ
###
import asyncio
import os
import random as ra
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from time import sleep

import bs4
import csv
import discord
import requests
from discord.ext import tasks

###
# 定義
###

# BotのAccess Token
TOKEN = os.environ["TOKEN"]

#
dict_response = {
    "/colorcorn": "<:colorcorn:627504593344921629>",
    "/neko": "にゃーん",
    "/unbobo": "うんぼぼうんぼぼウッホッホ！！！！💩💩💩💩💩💩",
    "/unpopo": "うーくん...あなたのことが好きです...。"
}

# ランダムで繰り返す単語辞書
dict_repetition = {
    "/kireji": [["ぶち", "ブチ"], "ィ", "ッ", "！", "💉"],
    "/shikko": [["ちょろ", "チョロ"], "💦"],
    "/unko": [["ぶり", "もり", "ぶぴ", "べちょ", "もぐ", "みち"], "ッ", "！", "💩"],
    "/washlet": [["ン゛"], "ッ", "！", "🙄💢"]
}

# スロットの単語辞書
#   word: どれか1要素が選ばれる
#           0番目は末尾に付ける単語
#   atari: key -> 当たりの単語,
#          value -> 当たったときの文
#                   クエリが存在すれば実行
#                   ""でクエリをランダムで実行
dict_slot = {
    "/aratan": {
        "word": ["", ["あら"], ["たん", "たそ", "くん", "ちゃん", "たそくんちゃん先輩"]],
        "atari": {
            "あらたん": ""
        }
    },
    "/daikon": {
        "word": ["", ["ダイ", "カラー"], ["コン", "コーン"]],
        "atari": {
            "ダイコン": "",
            "カラーコーン": "/colorcorn"
        }
    },
    "/hamako": {
        "word": ["ー", ["ハ", "ヒ", "フ", "ヘ", "ホ"], ["マ", "ミ", "ム", "メ", "モ"], ["カ", "キ", "ク", "ケ", "コ"]],
        "atari": {
            "ハマコー": ""
        }
    },
    "/omikuji" : {
        "word": ["便", ["大", "中", "吉", "小", "末", "凶", "大凶"]],
        "atari": {
            "大便": "/unko",
            "小便": "/shikko"
        }
    },
    "/satori": {
        "word": ["", ["うん"], ["ば", "び", "ぶ", "べ", "ぼ"], ["ば", "び", "ぶ", "べ", "ぼ"]],
        "atari": {
            "うんぼぼ": "/unbobo"
        }
    },
    "/zero": {
        "word": ["", ["ぜろ", "いち"], ["ホモ", "レズ", "ゲイ", "バイ"]],
        "atari": {
            "ぜろホモ": ""
        }
    }
}


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
        if type(rep) is str:  # string
            reply += rep * ra.randrange(40)
        else:  # list
            reply += ra.choice(rep) * ra.randrange(60)

    if qu == "/washlet":
        reply = "んっ...♥" if ra.randrange(100) > 20 else reply

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


def msg_dice(msg):
    """
    ダイス

    ----------
    qu: sting
        ダイス結果メッセージ
    """

    resplit = re.split('(\d+)d(\d+)', msg)
    n = int(resplit[1])
    me = int(resplit[2])

    # サイコロふる
    dice = [ra.randrange(me) + 1 for i in range(n)]
    # サイコロ2個以上なら合計を出力
    sum_ = "" if len(dice) == 1 else f"(sum: {sum(dice)})"

    return f"{', '.join(map(str, dice))} {sum_}"


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
    for msg in message.content.split('\n'):
        # 1回だけの応答用
        if msg in dict_response.keys():
            await message.channel.send(msg_response(msg))

        # 繰り返しの単語用
        if msg in dict_repetition.keys():
            await message.channel.send(msg_repetition(msg))

        # スロット
        if msg in dict_slot.keys() or msg == '/slot':
            await do_slot(msg, message)

        # ダイス
        if re.match('.*(\d+)d(\d+)', msg):
            await message.channel.send(msg_dice(msg))

        # おちんぽプログラム
        if '/ochinpo' in msg: # ochinpoが入っているとき( ◜◡＾)っ✂╰⋃╯
            arg_ = ''.join(msg.split()[1:])  # 引数
            PATTERN = '<:[0-9|a-z|_]+:[0-9]+>'  # カスタム絵文字の正規表現

            # 引数が指定されていれば、ターゲット文字列のカスタム絵文字を置換した文字列を作成
            # 引数が指定されていなければ、"おちんぽ"を入れる
            target = "おちんぽ" if len(arg_.split()) == 0 else re.sub(PATTERN, "-", arg_)
            # カスタム絵文字リスト
            emoji = re.findall(PATTERN, arg_)

            # ターゲット文字列リスト（カスタム絵文字＋文字）
            li_target = [emoji.pop(0) if q == '-' else q for q in list(target)]
            len_t = len(li_target)

            # ちっちゃいおちんぽだけ処理
            if len_t > 4:
                await message.channel.send("おちんぽおっきすぎだよぉ...")
            else:
                li_dumy_target = [f"unbobo{i}" for i in range(len_t)]  # おちんぽプログラムで使う文字列リスト
                target = "".join(li_dumy_target)  # おちんぽプログラムで使う文字列
                li_reply = [] # 出力結果リスト

                cnt = 0
                is_proc = True
                while is_proc:
                    # おちんぽシコリすぎないようにする
                    if cnt > 114514:
                        break

                    li_reply.append(ra.choice(li_dumy_target))
                    # ケツがターゲット文字列（ダミー）なら処理終了
                    is_proc = ''.join(li_reply[-len_t:]) != target

                    cnt += 1

                reply = ""
                for i, r in enumerate(li_reply):
                    reply += li_target[li_dumy_target.index(r)]

                    if (i+1) % 50 == 0:
                        await message.channel.send(reply)
                        reply = ""

                await message.channel.send(reply)
                await message.channel.send(f"おぉぉおﾞおﾞ～っ！！イグゥウ！！イッグゥウウ！！{cnt}回目で果てました...")

        # バーチャルコンテスト通知
        if 'https://not-522.appspot.com' in msg:
            link = msg
            get_url_info = requests.get(link)
            bs = bs4.BeautifulSoup(get_url_info.text, 'lxml')

            # タイトル
            title = bs.h1.get_text().lstrip().split()[0]
            # 開始時間取得
            line = bs.select('small')[0].text
            PATTERN = '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}'
            t_start, t_end = tuple(re.findall(PATTERN, line))

            await message.channel.send(f"💩バーチャルコンテスト開催のお知らせ💩\n**{title}**：{t_start}〜{t_end}\n{link}")

            with open("vc_alert.txt") as f:
                lines = [s.strip() for s in f.readlines()]

            lines.insert(0, f"{title}, {t_start}, {t_end}, {link}")

            await message.channel.send(lines)
            # unbobo

            with open("vc_alert.txt", mode='w') as f:
                f.writelines(lines)

        if msg == '/bbslot':
            ra_ = ra.randrange(83)

            with open("bb.txt") as f:
                l = f.readlines()

                # number, merit, comment
                sp = l[ra_].split(", ")

                s = sp[1].rstrip(', \n')
                await message.channel.send(f"{sp[0]}：{s}")

                if sp[2] is not "\n":
                    await message.channel.send(f"（ダ）：{sp[2]}")

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
            await message.channel.send(msg.replace('[unko]', msg_repetition("/unko")))


@client.event
async def on_ready():
    channel = client.get_channel(615869415103266817)  # AtCoder
    # channel = client.get_channel(632106376427995137) # 開発室

    while True:
        time_ = datetime.now(timezone(timedelta(hours=+9), 'JST'))

        if time_.strftime("%Y/%m/%d %H:%M") == "2019/11/03 22:20":
            await channel.send("【ぜーくん杯】まもなく開始です\nhttps://not-522.appspot.com/contest/6302209677459456")

        if time_.strftime("%Y/%m/%d %H:%M:%S") == "2019/11/03 23:50:00":
            await channel.send("【ぜーくん杯】終了です\nhttps://not-522.appspot.com/contest/6302209677459456")

        # await channel.send(time_.strftime("%Y/%m/%d %H:%M"))
        if time_.strftime("%Y/%m/%d %H:%M") == "2019/11/03 23:49":
            await asyncio.sleep(1)
        else:
            await asyncio.sleep(30)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
