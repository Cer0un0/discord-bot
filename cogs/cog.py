import bs4
import discord
import random as ra
import re
import requests
from discord.ext import commands


class Cog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。

    async def reply_mono(self, ctx, s):
        await ctx.send(s)

    async def reply_buriburi(self, ctx, li_):
        reply = ""
        for rep in li_:
            if type(rep) is str:  # string
                reply += rep * ra.randrange(40)
            else:  # list
                reply += ra.choice(rep) * ra.randrange(60)

        await ctx.send(reply)

    async def reply_slot(self, ctx, li_, bingo):
        reply = ""
        for li in li_[1:]:
            reply += ra.choice(li)

        # 末尾の単語を付ける
        await ctx.send(reply + li_[0])

        if reply + li_[0] == bingo:
            await self.reply_buriburi(ctx, [["ぶり", "もり", "ぶぴ", "べちょ", "もぐ", "みち"], "ッ", "！", "💩"])

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
    async def hkonro(self, ctx):
        """エッチコンロの火を灯す"""
        reply = "ｴ"
        reply += "ﾁ" * ra.randrange(100)
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
        """ウォシュレットを使う(33%の確率で前の人の水圧設定が激流葬)"""
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
        embed.add_field(name="/ochinpo [引数(max:4)]", value="公開オナニー", inline=False)
        embed.add_field(name="/omikuji", value="今日のウン勢", inline=False)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="文章埋め込み系", description="", color=0x8b4513)
        embed.add_field(name="\d+d\d+", value="賽は投げられた", inline=False)
        embed.add_field(name="[unko]", value="話してる途中で漏らぶりぶりぶりぶりぶりぶりぶり💩💩💩💩💩", inline=False)
        await ctx.send(embed=embed)

        embed = discord.Embed(title="常駐系", description="", color=0x8b4513)
        embed.add_field(name="(atcoder vcのリンク)", value="バチャコンの告知", inline=False)
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

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

                # await message.channel.send(lines)
                # unbobo

                with open("vc_alert.txt", mode='w') as f:
                    f.writelines(lines)

            if "[" in msg:
                replace = ""
                li_= [["ぶり", "もり", "ぶぴ", "べちょ", "もぐ", "みち"], "ッ", "！", "💩"]

                for rep in li_:
                    if type(rep) is str:  # string
                        replace += rep * ra.randrange(40)
                    else:  # list
                        replace += ra.choice(rep) * ra.randrange(60)

                await message.channel.send(msg.replace('[unko]', replace))



    # @commands.group()
    # async def role(self, ctx):
    #     # サブコマンドが指定されていない場合、メッセージを送信する。
    #     if ctx.invoked_subcommand is None:
    #         await ctx.send('このコマンドにはサブコマンドが必要です。')
    #
    # # roleコマンドのサブコマンド
    # # 指定したユーザーに指定した役職を付与する。
    # @role.command()
    # async def add(self, ctx, member: discord.Member, role: discord.Role):
    #     await member.add_roles(role)
    #
    # # roleコマンドのサブコマンド
    # # 指定したユーザーから指定した役職を剥奪する。
    # @role.command()
    # async def remove(self, ctx, member: discord.Member, role: discord.Role):
    #     await member.remove_roles(role)


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Cog(bot))
