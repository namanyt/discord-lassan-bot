from datetime import datetime
from random import randint, choice
from typing import Optional

from discord import Member, Embed
from discord.ext.commands import Cog, command
from discord.ext.menus import ListPageSource, MenuPages

from lib.bot import settings
from lib.db import db


class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx

        super().__init__(data, per_page=10)

    async def write_page(self, menu, offset, fields=[]):
        len_data = len(self.entries)

        embed = Embed(title="RICH BOII",
                      color=self.ctx.author.color)
        embed.set_thumbnail(url=self.ctx.guild.icon_url)
        embed.set_footer(text=f"{offset:,} - {min(len_data, offset + self.per_page - 1):,} of {len_data:,} members.")

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1

        fields = []
        table = ("\n".join(f"{idx+offset}. {self.ctx.bot.guild.get_member(entry[0]).display_name} (Wallet : {entry[1]})"
                           for idx, entry in enumerate(entries)))

        fields.append(("Ranks", table))

        return await self.write_page(menu, offset, fields)


class Economy(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="bal", aliases=['balance'])
    async def show_balance(self, ctx, target: Optional[Member]):
        target = target or ctx.author
        wallet, bank = db.record("SELECT Wallet, Bank FROM economy WHERE UserID = ?", target.id) or (None, None)
        if wallet is not None:
            pass
        else:
            db.execute("INSERT INTO economy (UserID) VALUES (?)", target.id)
            wallet, bank = db.record(f"SELECT Wallet, Bank FROM economy WHERE UserID = ?", target.id)

        wallet_embed = Embed(title="ECONOMY", timestamp=datetime.utcnow())
        wallet_embed.add_field(name=f"{target.display_name}'s Economy", value=f"Wallet: {wallet:,} \n Bank: {bank:, }",
                               inline=False)
        await ctx.send(embed=wallet_embed)

    @command(name='daily')
    async def daily_reward(self, ctx):
        wallet = db.record("SELECT Wallet FROM economy WHERE UserID = ?", ctx.author.id) or None

        daily_reward = 100

        if wallet is not None:
            db.execute("UPDATE economy SET Wallet = Wallet + ? WHERE UserID = ?", daily_reward, ctx.author.id)

            await ctx.send('here is your reward...')
            return
        else:
            db.execute("INSERT INTO economy (UserID) VALUES (?)", ctx.author.id)
            db.execute("UPDATE economy SET Wallet = Wallet + ? WHERE UserID = ?", daily_reward, ctx.author.id)
            await ctx.send('here is your reward...')
            return

    @command(name='beg')
    async def begging(self, ctx):
        wallet = db.record("SELECT Wallet FROM economy WHERE UserID = ?", ctx.author.id) or None
        ppl = ['Vivek', 'Charles', 'Alan', 'Queen', 'King', 'President', 'Dev']
        beg_money = randint(-100, 300)
        if beg_money <= 0:
            beg_money = 0
            await ctx.send(f"{choice(ppl)} -> No money for you !")
            if wallet is not None:
                db.execute("UPDATE economy SET Wallet = Wallet + ? WHERE UserID = ?", beg_money, ctx.author.id)
                return
            else:
                db.execute("INSERT INTO economy (UserID) VALUES (?)", ctx.author.id)
                db.execute("UPDATE economy SET Wallet = Wallet + ? WHERE UserID = ?", beg_money, ctx.author.id)
                await ctx.send('here is your reward...')
                return

        else:
            await ctx.send(f"{choice(ppl)} -> ${beg_money}, here you go.")
            if wallet is not None:
                db.execute("UPDATE economy SET Wallet = Wallet + ? WHERE UserID = ?", beg_money, ctx.author.id)
                return
            else:
                db.execute("INSERT INTO economy (UserID) VALUES (?)", ctx.author.id)
                db.execute("UPDATE economy SET Wallet = Wallet + ? WHERE UserID = ?", beg_money, ctx.author.id)
                await ctx.send('here is your reward...')
                return

    @command(name='rob', aliases=['steal'])
    async def rob_other_users(self, ctx, target: Member = None):
        wut = self.bot.get_emoji(settings['emojis']['wut'])
        if target is None:
            await ctx.send(f"{wut} who is the user bro !")
            return

        target_bal = db.record("SELECT Wallet FROM economy WHERE UserID = ?", target.id) or None
        if target_bal is None:
            await ctx.send("That user doesn't have a bank account")
            return

        user_bal = db.record("SELECT Wallet FROM economy WHERE UserID = ?", ctx.author.id) or None
        if user_bal is None:
            db.execute("INSERT INTO economy (UserID) VALUES (?)", ctx.author.id)

        loot = randint(1, 100)
        chances = randint(1, 100)

        if chances <= 50:
            await ctx.send("You got caught by the police")
            await ctx.send(f"Now u have to pay {loot} to {target.display_name}")
            db.execute("UPDATE economy SET Wallet = Wallet - ? WHERE UserID = ?", loot, ctx.author.id)
            db.execute("UPDATE economy SET Wallet = Wallet + ? WHERE UserID = ?", loot, target.id)
            return

        db.execute("UPDATE economy SET Wallet = Wallet + ? WHERE UserID = ?", loot, ctx.author.id)
        db.execute("UPDATE economy SET Wallet = Wallet - ? WHERE UserID = ?", loot, target.id)
        await ctx.send(f"You robbed ${loot} from {target.display_name}")

    @command(name='rich', aliases=['moneylb'])
    async def rich_users(self, ctx):
        records = db.records("SELECT UserID, Wallet FROM economy ORDER BY Wallet DESC")

        menu = MenuPages(source=HelpMenu(ctx, records),
                         clear_reactions_after=True,
                         timeout=60.0)
        await menu.start(ctx)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("economy")


def setup(bot):
    bot.add_cog(Economy(bot))
