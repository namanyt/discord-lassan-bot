from datetime import datetime, timedelta
from typing import Optional
from json import load, dump
from discord import Member, Role
from discord import Member
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import command, has_permissions, bot_has_permissions
from discord.ext.commands import cooldown, BucketType

from lib.bot import settings
from lib.db import db


class Mod(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="clear", aliases=["purge"])
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    @cooldown(1, 2, type=BucketType.user)
    async def clear_messages(self, ctx, targets: Greedy[Member], limit: Optional[int] = 1):
        def _check(message):
            return not len(targets) or message.author in targets

        if 0 < limit <= 100:
            with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=limit, after=datetime.utcnow() - timedelta(days=365),
                                                  check=_check)

                await ctx.send(f"Deleted {len(deleted):,} messages.", delete_after=5)

        else:
            await ctx.send("The limit provided is not within acceptable bounds. (Less than 100)")

    @command(name='mute')
    async def mute_member(self, ctx, member: Member = None):
        if member is None:
            await ctx.send('do it again, but also put the name of the member to mute', delete_after=2)
            return

        try:
            db.execute("INSERT INTO mutes (UserID) VALUES (?)", member.id)
        except:
            pass

        is_muted = db.record("SELECT mute FROM mutes WHERE UserID = ?", member.id)
        if is_muted == (1,):
            await ctx.send(f'{member.display_name} is already muted')
            return

        await member.add_roles(member.guild.get_role(settings['roles']['mute']))
        db.execute("UPDATE mutes SET mute = mute + ? WHERE UserID = ?", 1, member.id)

    @command(name='unmute')
    async def unmute_member(self, ctx, member: Member = None):
        if member is None:
            await ctx.send('do it again, but also put the name of the member to unmute', delete_after=2)
            return

        try:
            db.execute("INSERT INTO mutes (UserID) VALUES (?)", member.id)
        except:
            pass

        is_muted = db.record("SELECT mute FROM mutes WHERE UserID = ?", member.id)
        if is_muted == (0,):
            await ctx.send(f'{member.display_name} is already unmuted')
            return

        await member.remove_roles(member.guild.get_role(settings['roles']['mute']))
        db.execute("UPDATE mutes SET mute = mute - ? WHERE UserID = ?", 1, member.id)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")


def setup(bot):
    bot.add_cog(Mod(bot))
