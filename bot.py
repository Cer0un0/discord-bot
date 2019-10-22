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

    await message.channel.send(message)
    await message.channel.send(str(discord.Client.emojis[1]))
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
        if '/ochinpo' in msg: # おちんぽが入っているとき( ◜◡＾)っ✂╰⋃╯
            query = "おちんぽ" if len(msg.split()) == 1 else msg.split()[1]
            await message.channel.send(f"Query: {query} Length: {len(query)}")

            if len(query) > 5: # おちんぽおっきいときは処理してあげない
                await message.channel.send("おちんぽおっきすぎだよぉ...")
            else:# おちんぽちっちゃいときは処理
                cnt = 0
                is_proc = True
                reply = ""
                while is_proc:
                    # おちんぽシコリすぎないようにする
                    if cnt > 3000:
                        break

                    reply += ra.choice(list(query))
                    is_proc = (reply[-len(query):] != query)

                    cnt += 1

                await message.channel.send(reply)
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
            await message.channel.send(msg.replace('[unko]', msg_repetition("/unko")))


        # if ":poop" in msg:
        #     reply = ""
        #     reply += "ぶり" * [msg.count(":poop")]
        #     reply += "っ"
        #     await message.channel.send(reply)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
