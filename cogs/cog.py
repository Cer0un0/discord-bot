import re
import random as ra

import bs4
import discord
import gspread
import requests
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials


class Cog(commands.Cog):
    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.last_account = "human"

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。

    async def reply_mono(self, ctx, s):
        await ctx.send(s)

    async def reply_buriburi(self, ctx, li_, max_buriburi=40, max_unchi=60):
        reply = ""
        for rep in li_:
            if type(rep) is str:  # string
                reply += rep * ra.randrange(1, max_buriburi)
            else:  # list
                reply += ra.choice(rep) * ra.randrange(1, max_unchi)

        await ctx.send(reply)

    async def reply_slot(self, ctx, li_, bingo):
        reply = ""
        for li in li_[1:]:
            reply += ra.choice(li)

        # 末尾の単語を付ける
        await ctx.send(reply + li_[0])

        if reply + li_[0] == bingo:
            await self.reply_buriburi(ctx, [["ぶり", "ぼと", "もり", "ぶぴ", "べちょ", "もぐ", "みち"], "ッ", "！", "💩"])

    async def _lpgacha(self, ctx):
        link = "https://loveplus-every.boom-app.wiki"

        # カードリストの中からランダムに選ぶ
        bs = bs4.BeautifulSoup(requests.get(f"{link}/entry/card-list").text, 'lxml')
        rows = bs.findAll("table")[ra.randrange(1, 10)].findAll("tr")
        card_id = rows[ra.randrange(1, len(rows))].td.a.get("href")

        # カードのページから画像のURLを取得
        bs2 = bs4.BeautifulSoup(requests.get(f"{link}{card_id}").text, 'lxml')
        name, type_, rare, _, _ = [tr.td.string for tr in bs2.findAll("table")[0].findAll("tr")]
        imglink = bs2.find("div", class_="imgList1").div.div.get("data-url")

        await ctx.send(f"[{type_}] {name} {rare}\n{imglink}")

    # reply_mono
    @commands.command()
    async def colorcorn(self, ctx):
        """カラーコーンを放流する"""
        await self.reply_mono(ctx, "<:colorcorn:627504593344921629>")

    @commands.command()
    async def neko(self, ctx):
        """社会性フィルターを通して社会の不条理を嘆く"""
        await self.reply_mono(ctx, "にゃーん")

    @commands.command()
    async def unbobo(self, ctx):
        """うんぼぼ一族とコミュニケーションを取る"""
        await self.reply_mono(ctx, "うんぼぼうんぼぼウッホッホ！！！！💩💩💩💩💩💩")

    @commands.command()
    async def unpopo(self, ctx):
        """凛子の告白を思い返す"""
        await self.reply_mono(ctx, "うーくん...あなたのことが好きです...。")

    @commands.command()
    async def hkonro(self, ctx, max_chi=100):
        """エッチコンロの火を灯す"""
        reply = "ｴ"
        reply += "ﾁ" * ra.randrange(1, max_chi)
        await ctx.send(f"エッチコンロ点火！{reply}勃ッ！！！！！！！！！！！！！！🔥")


    # reply_buriburi
    @commands.command()
    async def kireji(self, ctx):
        """切れ痔の人の気持ちを知る"""
        await self.reply_buriburi(ctx, [["ぶち", "ブチ"], "ィ", "ッ", "！", "💉"])

    @commands.command()
    async def shikko(self, ctx):
        """漏らす"""
        await self.reply_buriburi(ctx, [["ちょろ", "チョロ"], "💦"])

    @commands.command()
    async def unko(self, ctx):
        """漏らす"""
        await self.reply_buriburi(ctx, [["ぶり", "もり", "ぶぴ", "べちょ", "もぐ", "みち"], "ッ", "！", "💩"])

    @commands.command()
    async def washlet(self, ctx):
        """ウォシュレットを使う(33%の確率で前に使った人の水圧設定がアホ)"""
        if ra.randrange(100) > 33:
            await ctx.send("んっ...♥")
        else:
            await self.reply_buriburi(ctx, [["ン゛"], "ッ", "！", "🙄💢"])

    # TODO: reply_slot
    # @commands.command()
    # async def aratan(self, ctx):
    #     """あらたんスロット(20%)"""
    #     await self.reply_buriburi(ctx, ["", ["あら"], ["たん", "たそ", "くん", "ちゃん", "たそくんちゃん先輩"]])

    @commands.command()
    async def omikuji(self, ctx):
        """今日のウン勢"""
        await self.reply_slot(ctx, ["便", ["大", "中", "吉", "小", "末", "凶", "大凶"]], "大便")

    @commands.command()
    async def lpgacha(self, ctx):
        await self._lpgacha(ctx)

    async def insert_vcdata(self, vcdata):
        title, t_start, t_end, link = vcdata

        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name('gspread.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open('DiscordBot').worksheet('virtual-contest')

        wks.update_acell('A1', title)
        wks.update_acell('B1', t_start[:-3])
        wks.update_acell('C1', t_end[:-3])
        wks.update_acell('D1', link)

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="単一応答系", description="", color=0x8b4513)
        embed.add_field(name="/colorcorn", value="カラーコーンを放流する", inline=False)
        embed.add_field(name="/help", value="これ", inline=False)
        embed.add_field(name="/hkonro", value="エッチコンロの火を灯す", inline=False)
        embed.add_field(name="/neko", value="社会性フィルターを通して社会の不条理を嘆く", inline=False)
        embed.add_field(name="/unbobo", value="うんぼぼ一族とコミュニケーションを取る", inline=False)
        embed.add_field(name="/unpopo", value="凛子の告白を思い返す", inline=False)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="ぶりつき系", description="", color=0x8b4513)
        embed.add_field(name="/kireji", value="切れ痔の気持ちになれ", inline=False)
        embed.add_field(name="/shikko", value="漏らす", inline=False)
        embed.add_field(name="/unko", value="漏らす", inline=False)
        embed.add_field(name="/washlet", value="ウォシュレットを使う(33%の確率で前に使った人の水圧設定がアホ)", inline=False)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="スロット系", description="", color=0x8b4513)
        embed.add_field(name="/lpgacha", value="カノジョの画像でシコる", inline=False)
        embed.add_field(name="/ochinpo [引数(max:4)]", value="公開オナニー", inline=False)
        embed.add_field(name="/omikuji", value="今日のウン勢", inline=False)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="文章埋め込み系", description="", color=0x8b4513)
        embed.add_field(name="\d+d\d+", value="賽は投げられた", inline=False)
        embed.add_field(name="[unko]", value="話してる途中で漏らぶりぶりぶりぶりぶりぶりぶり💩💩💩💩💩", inline=False)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="常駐系", description="", color=0x8b4513)
        embed.add_field(name="atcoder vcのリンク", value="バチャコンの告知", inline=False)
        embed.add_field(name="[凛子|寧々|愛花]", value="lpgacha (\"！\"でエスケープ)", inline=False)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            self.last_account = "bot"
            return
        else:
            self.last_account = "human"

        for msg in message.content.split('\n'):
            if re.match('.*(\d+)d(\d+)', msg):
                resplit = re.split('(\d+)d(\d+)', msg)
                n = int(resplit[1])
                me = int(resplit[2])

                # サイコロふる
                dice = [ra.randrange(me) + 1 for i in range(n)]
                # サイコロ2個以上なら合計を出力
                sum_ = "" if len(dice) == 1 else f"(sum: {sum(dice)})"

                await message.channel.send(f"{', '.join(map(str, dice))} {sum_}")

            # おちんぽプログラム
            if '/ochinpo' in msg:  # ochinpoが入っているとき( ◜◡＾)っ✂╰⋃╯
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
                    li_reply = []  # 出力結果リスト

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

                        if (i + 1) % 50 == 0:
                            await message.channel.send(reply)
                            reply = ""

                    await message.channel.send(reply)
                    await message.channel.send(f"おぉぉおﾞおﾞ～っ！！イグゥウ！！イッグゥウウ！！{cnt}回目で果てました...")

            # alert Virtual Contest
            if 'https://not-522.appspot.com' in msg:
                # get VC information from link
                link = msg
                get_url_info = requests.get(link)
                bs = bs4.BeautifulSoup(get_url_info.text, 'lxml')
                header = bs.h1.text
                lines = header.split('\n')
                TIME_PATTERN = '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}'

                # get information
                title = lines[1].lstrip()
                t_start, t_end = re.findall(TIME_PATTERN, lines[2])

                # post
                await message.channel.send(f"💩バーチャルコンテスト開催のお知らせ💩\n**{title}**\n{t_start[:-3]}〜{t_end[:-3]}")

                # insert spread sheet
                await self.insert_vcdata((title, t_start, t_end, link))

            # 話してる途中でうんこ漏らす
            if "[" in msg:
                replace = ""
                li_ = [["コロ", "ぶぴ", "ぶり", "びちゃ", "べちょ", "ぼと", "みち", "もぐ", "もり"], "ッ", "！", "💩"]

                for rep in li_:
                    if type(rep) is str:  # string
                        replace += rep * ra.randrange(40)
                    else:  # list
                        replace += ra.choice(rep) * ra.randrange(60)

                await message.channel.send(msg.replace('[unko]', replace))

            # 呼びかけてlpgacha引く
            if any(map(msg.__contains__, ("凛子", "寧々", "愛花"))):
                if "！" not in msg:
                    await self._lpgacha(message.channel)


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Cog(bot))
