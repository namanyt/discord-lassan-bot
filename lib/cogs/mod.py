from datetime import datetime, timedelta
from typing import Optional
from json import load, dump
from discord import Member, Role
from discord import Member
from discord.ext.commands import Cog, Greedy
from discord.ext.commands import command, has_permissions, bot_has_permissions
from discord.ext.commands import cooldown, BucketType

from lib.bot import settings


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

    async def open_warnsheet(self):
        with open("./data/json/warn.json", "r") as f:
            warn = load(f)
        return warn

    async def open_user_warnsheet(self, user: Greedy[Member]):
        warn = await self.open_warnsheet()

        if str(user.id) in warn:
            return False
        else:
            warn[str(user.id)] = {}
            warn[str(user.id)]["name"] = user.display_name
            warn[str(user.id)]["warn"] = 100

        with open("./data/json/warn.json", "w") as f:
            dump(warn, f)
        return True

    @command(name='mute')
    @cooldown(1, 2, type=BucketType.user)
    async def mute_members(self, ctx, member: Member = None):
        if member is None:
            await ctx.send('do it again but put the mention the member too', delete_after=3)
            return
        user = member
        mute_role = ctx.guild.get_role(settings['roles']['mute'])
        await self.open_user_warnsheet(user)
        warn = await self.open_warnsheet()

        if warn[str(user.id)]['warn'] == 1:
            await ctx.send(f'{member.display_name} is already muted', delete_after=3)
            return

        warn[str(user.id)]['warn'] = 1

        await ctx.send(f'muted {member.display_name}', delete_after=3)
        await member.add_roles(mute_role)
        with open('./data/json/warn.json', 'w') as f:
            dump(warn, f)
        return True

    @command(name='unmute')
    @cooldown(1, 2, type=BucketType.user)
    async def unmute_member(self, ctx, member: Member = None):
        if member is None:
            await ctx.send('do it again but put the mention the member too', delete_after=3)
            return
        user = member
        mute_role = ctx.guild.get_role(settings['roles']['mute'])
        await self.open_user_warnsheet(user)
        warn = await self.open_warnsheet()

        if warn[str(user.id)]['warn'] == 0:
            await ctx.send(f'{member.display_name} member is not mute', delete_after=3)
            return False

        warn[str(user.id)]['warn'] = 0
        await ctx.send(f'{member.display_name} unmuted', delete_after=3)
        await member.remove_roles(mute_role)
        with open('./data/json/warn.json', 'w') as f:
            dump(warn, f)
        return True

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")


def setup(bot):
    bot.add_cog(Mod(bot))
