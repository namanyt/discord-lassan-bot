from discord import Member, Guild
from discord.ext.commands import Cog, command, cooldown, BucketType
from discord.utils import get

from lib.bot import settings


class Voice(Cog):
    def __init__(self, bot):
        self.bot = bot

    temp_VC = []

    @command(name='name')
    @cooldown(1, 200, BucketType.user)
    async def change_VC_name(self, ctx, *, name: str = None):
        voice_state = ctx.author.voice
        channel = voice_state.channel
        if voice_state is None:
            await ctx.send('you need to be in a temp voice channel to run this command')
            return

        temp_channels = self.temp_VC

        for temp_channel in temp_channels:
            if channel.id == temp_channel:
                await channel.edit(name=name)
                await ctx.send(f'successfully changed name to {name}')

    @command(name='limit')
    @cooldown(1, 200, BucketType.user)
    async def change_VC_limit(self, ctx, limit: int):
        voice_state = ctx.author.voice
        channel = voice_state.channel
        if voice_state is None:
            await ctx.send('you need to be in a temp voice channel to run this command')
            return

        temp_channels = self.temp_VC

        for temp_channel in temp_channels:
            if channel.id == temp_channel:
                await channel.edit(user_limit=limit)
                await ctx.send(f'successfully set {limit} limit')

    @command(name='lock')
    @cooldown(1, 200, BucketType.user)
    async def locking_VC(self, ctx):
        voice_state = ctx.author.voice
        channel = voice_state.channel
        if voice_state is None:
            await ctx.send('you need to be in a temp voice channel to run this command')
            return

        temp_channels = self.temp_VC

        for temp_channel in temp_channels:
            if channel.id == temp_channel:
                await channel.edit(user_limit=1)
                await ctx.send('locked VC')

    @command(name='unlock')
    @cooldown(1, 200, BucketType.user)
    async def unlocking_VC(self, ctx):
        voice_state = ctx.author.voice
        channel = voice_state.channel
        if voice_state is None:
            await ctx.send('you need to be in a temp voice channel to run this command')
            return

        temp_channels = self.temp_VC

        for temp_channel in temp_channels:
            if channel.id == temp_channel:
                await channel.edit(user_limit=0)
                await ctx.send('Unlocked the VC')

    @Cog.listener()
    async def on_voice_state_update(self, member: Member, before, after):
        if member.bot:
            return

        if not before.channel:
            await member.add_roles(member.guild.get_role(settings['roles']['in_vc']))

        if before.channel and not after.channel:
            await member.remove_roles(member.guild.get_role(settings['roles']['in_vc']))

        if after.channel is not None:
            if after.channel.id == settings['channel']['p_vc']:
                for guild in self.bot.guilds:
                    maincategory = get(
                        guild.categories, id=settings['channel']['p_vc_cat'])
                    channel2 = await guild.create_voice_channel(name=f'{member.display_name}\'s channel',
                                                                category=maincategory)
                    await channel2.set_permissions(member, connect=True, mute_members=True, manage_channels=True)
                    await member.move_to(channel2)
                    self.temp_VC.append(channel2.id)

                    def check(x, y, z):
                        return len(channel2.members) == 0

                    await self.bot.wait_for('voice_state_update', check=check)
                    await channel2.delete()
                    self.temp_VC.remove(channel2.id)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('voice')


def setup(bot):
    bot.add_cog(Voice(bot))
