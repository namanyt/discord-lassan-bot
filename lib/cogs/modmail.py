from datetime import datetime

from discord import Embed, Color
from discord.ext.commands import Cog

from lib.bot import settings


class ModMail(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if str(message.channel.type) == "private":
            mod_mail_channel = self.bot.get_channel(settings["channel"]['mod_mail'])

            ModMailMessageEmbed = Embed(title="Mod Mail", description=f"from {message.author.name}",
                                        timestamp=datetime.utcnow(), color=Color.random())

            ModMailMessageEmbed.add_field(name='Help !', value=f'{message.content}', inline=False)

            await mod_mail_channel.send(embed=ModMailMessageEmbed)

        elif str(message.channel) == "stdout-mod-mail" and message.content.startswith("<"):
            member_object = message.mentions[0]
            index = message.content.index(" ")
            string = message.content
            mod_message = string[index:]

            await member_object.send(f"{mod_message}")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("modmail")


def setup(bot):
    bot.add_cog(ModMail(bot))
