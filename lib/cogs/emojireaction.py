from discord.ext.commands import Cog

from lib.bot import settings


class Emojireaction(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("emojireaction")

    @Cog.listener()
    async def on_message(self, message):
        good_Word = ["gg", "-_-", "gm", "bye", "yeah boi", "boiii", "XD", ";-;", "^_^", "sorry", "noob", "sry"]
        reaction_in_announcements = self.bot.get_emoji(settings['emojis']['sleepy_boi'])
        announcements_channel = self.bot.get_channel(settings['channel']['announcements'])

        if message.content:
            if ":" == message.content[0] and ":" == message.content[-1]:
                emoji_name = message.content[1:-1]
                for emoji in message.guild.emojis:
                    if emoji_name == emoji.name:
                        await message.channel.send(f"{str(emoji)}")
                        await message.channel.send(f"{message.author.mention}")
                        await message.delete()
                        break

        if message.channel.id == announcements_channel.id:
            await message.add_reaction(reaction_in_announcements)

        if message.author.id == self.bot.user.id:
            return

        for word in good_Word:
            if word.lower() in message.content == "gg".lower():
                c = message.channel.id
                channel = self.bot.get_channel(c)
                await channel.send("GG")

            elif word.lower() in message.content == "noob".lower():
                c = message.channel.id
                channel = self.bot.get_channel(c)
                await channel.send("w o w")

            elif word.lower() in message.content == "sorry".lower():
                c = message.channel.id
                channel = self.bot.get_channel(c)
                await channel.send("no problem")

            elif word.lower() in message.content == "sry".lower():
                c = message.channel.id
                channel = self.bot.get_channel(c)
                await channel.send("no problem 🙂")

            elif word.lower() in message.content == "-_-":
                await message.add_reaction("🤯")

            elif word.lower() in message.content == "gm".lower():
                c = message.channel.id
                channel = self.bot.get_channel(c)
                await channel.send("Gm")

            elif word.lower() in message.content == "bye".lower():
                c = message.channel.id
                channel = self.bot.get_channel(c)
                await channel.send("Goodbye")

            elif word.lower() in message.content == "yeah boi".lower():
                await message.add_reaction("🙂")

            elif word.lower() in message.content == "boiii".lower():
                await message.add_reaction("🤔")

            elif word in message.content == "XD":
                await message.add_reaction("😆")

            elif word.lower() in message.content == ";-;".lower():
                await message.add_reaction("😭")

            elif word.lower() in message.content == "^_^".lower():
                await message.add_reaction("🤪")


def setup(bot):
    bot.add_cog(Emojireaction(bot))
