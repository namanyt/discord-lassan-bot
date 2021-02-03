from discord.ext import commands
from discord.ext.commands import Cog, command


class Shutdown(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @command(name='off', aliases=['shutdown'])
    async def shutdown(self, ctx):
        await ctx.send("Adios")
        await self.bot.logout()

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("shutdown")


def setup(bot):
    bot.add_cog(Shutdown(bot))
