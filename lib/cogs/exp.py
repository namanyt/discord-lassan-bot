from asyncio import sleep
from datetime import datetime, timedelta
from io import BytesIO
from os import remove
from os.path import isfile
from typing import Optional

from PIL import Image, ImageFont, ImageDraw, ImageOps
from discord import Member, Embed, File
from discord.ext.commands import Cog, command, cooldown, BucketType
from discord.ext.menus import ListPageSource, MenuPages
from requests import get

from ..db import db


class HelpMenu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx

        super().__init__(data, per_page=10)

    async def write_page(self, menu, offset, fields=[]):
        len_data = len(self.entries)

        embed = Embed(title="XP Leaderboard",
                      colour=self.ctx.author.colour)
        embed.set_thumbnail(url=self.ctx.guild.icon_url)
        embed.set_footer(text=f"{offset:,} - {min(len_data, offset + self.per_page - 1):,} of {len_data:,} members.")

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1

        fields = []
        table = ("\n".join(
            f"{idx + offset}. {self.ctx.bot.guild.get_member(entry[0]).display_name} (XP: {entry[1]} | Level: {entry[2]})"
            for idx, entry in enumerate(entries)))

        fields.append(("Ranks", table))

        return await self.write_page(menu, offset, fields)


class Exp(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def process_xp(self, msg):
        xp, lvl, xplock = db.record("SELECT XP, LEVEL, XPLOCK FROM exp WHERE UserID = ?", msg.author.id)

        if msg.content == "+level":
            pass
        elif msg.content == "+rank":
            pass
        else:
            await self.add_xp(msg, xp, lvl)

    async def add_xp(self, message, xp, lvl):
        xp_to_add = 1
        new_lvl = int(xp // 25)

        db.execute("UPDATE exp SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?",
                   xp_to_add, new_lvl, (datetime.utcnow() + timedelta(seconds=60)).isoformat(), message.author.id)

        if new_lvl > lvl:
            await message.channel.send(f"Congrats {message.author.mention} - you reached level {new_lvl:,}!")

    @command(name="level")
    @cooldown(1, 2, BucketType.user)
    async def display_level(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        xp, lvl = db.record("SELECT XP, Level FROM exp WHERE UserID = ?", target.id) or (None, None)

        if lvl is not None:
            embed = Embed(title='EXPERIENCE', timestamp=datetime.utcnow())
            embed.add_field(name=f'{target.display_name}\'s Level', value=f'Level: {lvl:,} \n Xp: {xp:,}')
            await ctx.send(embed=embed)

        else:
            await ctx.send("That member is not tracked by the experience system.")

    @command(name="rank")
    @cooldown(1, 2, BucketType.user)
    async def display_rank(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        ids = db.column("SELECT UserID FROM exp ORDER BY XP DESC")

        try:
            await ctx.send(f"{target.display_name} is rank {ids.index(target.id) + 1} of {len(ids)}.")

        except ValueError:
            await ctx.send("That member is not tracked by the experience system.")

    @command(name="leaderboard", aliases=["lb"])
    @cooldown(1, 2, BucketType.user)
    async def display_leaderboard(self, ctx):
        records = db.records("SELECT UserID, XP, Level FROM exp ORDER BY XP DESC")

        menu = MenuPages(source=HelpMenu(ctx, records),
                         clear_reactions_after=True,
                         timeout=60.0)
        await menu.start(ctx)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("exp")

    @Cog.listener()
    async def on_message(self, msg):
        if not msg.author.bot:
            if not str(msg.channel.type) == "private":
                await self.process_xp(msg)


def setup(bot):
    bot.add_cog(Exp(bot))
