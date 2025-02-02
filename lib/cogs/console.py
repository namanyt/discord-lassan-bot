from discord import TextChannel
from discord.ext.commands import Cog
from discord.ext.commands import command

from lib.bot import settings


class Console(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='send')
    async def send_message(self, ctx, channel: TextChannel = None, *, message: str = None):
        if channel is None:
            await ctx.send('please mention the channel to send', delete_after=2)
            return
        elif message is None:
            await ctx.send('please put some message to send', delete_after=2)
            return
        await channel.send(message)
        return

    @Cog.listener()
    async def on_message(self, message):
        console_channel = self.bot.get_channel(settings['channel']['console'])
        if message.author.id == self.bot.user.id:
            return

        else:
            if message.channel.id == console_channel.id:
                if message.content.startswith("<#"):
                    channel_object = message.channel_mentions[0]
                    index = message.content.index(" ")
                    string = message.content
                    console_message = string[index:]

                    await channel_object.send(f"{console_message}")

            if '<@' in message.content:
                await console_channel.send(f"{message.author} --> {message.content}")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('console')


def setup(bot):
    bot.add_cog(Console(bot))
