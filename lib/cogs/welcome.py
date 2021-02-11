from datetime import datetime

from discord import Forbidden, Embed
from discord.ext.commands import Cog

from ..bot import settings
from ..db import db


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
        db.execute("INSERT INTO economy (UserID) VALUES (?)", member.id)
        welcome_embed = Embed(title="WELCOME", timestamp=datetime.utcnow(),
                              description=f"Welcome {member.mention} ! \n ** **\n Head over to <#{settings['channel']['general']}> to say HI \n ** ** \n"
                                          f"***Total Member: {member.guild.member_count}***")

        welcome_embed.set_thumbnail(url=member.avatar_url)
        await self.bot.get_channel(settings['channel']['welcome']).send(embed=welcome_embed)

        try:
            await member.send(f"Welcome to **{member.guild.name}**! Enjoy your stay!")

        except Forbidden:
            pass

        await member.add_roles(member.guild.get_role(settings['roles']['friend']))

    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
        db.execute("INSERT INTO economy (UserID) VALUES (?)", member.id)
        await self.bot.get_channel(settings['channel']['goodbye']).send(
            f"{member.display_name} has left {member.guild.name}.")


def setup(bot):
    bot.add_cog(Welcome(bot))
