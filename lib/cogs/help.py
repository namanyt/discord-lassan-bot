from discord import Embed, Color, utils, Member, Role
from discord.ext.commands import Cog
from discord.ext.commands import command

from lib.bot import settings


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @command(name='help', aliases=['h', '?'])
    async def help_command(self, ctx, help_type: str = None):
        # main help set
        if not help_type:
            embed = Embed(title="HELP MENU",
                          description=f"put `{self.bot.PREFIX}` before the command for the bot to see the command",
                          color=Color.random())
            inline = True
            coolBoi = self.bot.get_emoji(settings['emojis']['cool_boi'])
            embed.add_field(name='1. 💰 Economy 💰', value=f'type `{self.bot.PREFIX}help economy`', inline=inline)
            embed.add_field(name='2. ⚙️ ️help_typeration ⚙️', value=f'type `{self.bot.PREFIX}help mod`', inline=inline)
            embed.add_field(name='3. ⬆️ Level ⬆️', value=f'type `{self.bot.PREFIX}help level`', inline=inline)
            embed.add_field(name=f'4. {coolBoi} Fun {coolBoi}', value=f'type `{self.bot.PREFIX}help fun`', inline=inline)

            embed.add_field(name='5. 🖥️ Server 🖥️', value=f'type `{self.bot.PREFIX}help server`', inline=inline)
            embed.add_field(name='6. 🔈 Voice 🔈', value=f'type `{self.bot.PREFIX}help vc`', inline=inline)
            embed.add_field(name='Still need help ?', value='DM me and I will try to reply as soon as possible :smile:',
                            inline=False)
            embed.set_footer(text='thing in `<>` are necessary, and `()` are optional')
            await ctx.send(embed=embed)

        # each help type
        elif help_type == "vc":
            pass
            embed_vc = Embed(title="HELP MENU",
                             description='For VC commands\n (you have to be in a VC to use these commands)',
                             color=Color.random())
            inline_vc = False
            embed_vc.add_field(name='📛 Change Name 📛', value=f'`{self.bot.PREFIX}name <name>` for changing the name of VC',
                               inline=inline_vc)
            embed_vc.add_field(name='🛃 Set Limit 🛃', value=f'`{self.bot.PREFIX}limit <limit>` for changing the limit of VC',
                               inline=inline_vc)
            embed_vc.add_field(name='🛑 Lock VC 🛑', value=f'`{self.bot.PREFIX}lock` to lock the VC you are in.',
                               inline=inline_vc)
            embed_vc.add_field(name='🟢 Unlock VC 🟢', value=f'`{self.bot.PREFIX}unlock` to unlocking the VC you are in',
                               inline=inline_vc)
            await ctx.send(embed=embed_vc)

        elif help_type == "fun":
            gud = self.bot.get_emoji(settings['emojis']['gud'])
            cute = self.bot.get_emoji(settings['emojis']['cute_cat'])
            doot = self.bot.get_emoji(settings['emojis']['doot'])
            cute_hi = self.bot.get_emoji(settings['emojis']['CuteDragonHi'])
            embed_fun = Embed(title="HELP MENU", description="for fun commands", color=Color.random())
            inline_fun = False
            embed_fun.add_field(name=f'😵 Kill 😵',
                                value=f'`{self.bot.PREFIX}kill <user>` to kill the user (not actaully)',
                                inline=inline_fun)
            embed_fun.add_field(name=f'{cute_hi} hello {cute_hi}', value=f'`{self.bot.PREFIX}hello`, Hello !', inline=inline_fun)
            embed_fun.add_field(name='lenny', value=f'`{self.bot.PREFIX}lenny`, just do it !', inline=inline_fun)
            embed_fun.add_field(name=f'{cute} cute {cute}', value=f'`{self.bot.PREFIX}cute`, just do it !', inline=inline_fun)
            embed_fun.add_field(name=f'{doot} doot {doot}', value=f'`{self.bot.PREFIX}doot <message>`, give a nice design to message',
                                inline=inline_fun)
            embed_fun.add_field(name=f'{gud} dankrate {gud}', value=f'`{self.bot.PREFIX}drankrate`, tell your dankrate.',
                                inline=inline_fun)
            embed_fun.add_field(name='💻 hack 💻', value=f'`{self.bot.PREFIX}hack <user>`, hacks the user.',
                                inline=inline_fun)
            embed_fun.add_field(name='🗣️ say 🗣️', value=f'`{self.bot.PREFIX}say <message>`, says a message',
                                inline=inline_fun)
            await ctx.send(embed=embed_fun)

        elif help_type == "server":
            inline_server = False
            embed_server = Embed(title='HELP MENU', description='for help regarding the server', color=Color.random())
            embed_server.add_field(name='Rule',
                                   value=
                                   'https://discord.com/channels/732263342181187595/765829498175356968/784747350815408138',
                                   inline=inline_server)
            embed_server.add_field(name='Owner', value=f'<@{settings["owner"]}> is our owner')
            embed_server.add_field(name='Bot Developer', value=f'<@{settings["dev"]}> is my developer')
            embed_server.add_field(name='More Help',
                                   value='if need more help DM me and i will try to reply as soon as possible ! :smile:')
            await ctx.send(embed=embed_server)

        elif help_type == "economy":
            embed_economy = Embed(title="HELP MENU", description="for Economy", color=Color.random())
            inline_economy = False

            embed_economy.add_field(name=f"🏦 BALANCE",
                                    value=f"`{self.bot.PREFIX}bal (user)` to see the balance of your / user's account",
                                    inline=inline_economy)
            embed_economy.add_field(name=f"🗓️ DAILY",
                                    value=f"`{self.bot.PREFIX}daily` or `/d` to get your daily reward",
                                    inline=inline_economy)
            embed_economy.add_field(name=f'BEG', value=f'`{self.bot.PREFIX}beg` to beg money.', inline=inline_economy)
            embed_economy.add_field(name=f"📝 WITHDRAW",
                                    value=f"`{self.bot.PREFIX}withdraw <amount>` or `{self.bot.PREFIX}withdraw all` to withdraw money",
                                    inline=inline_economy)
            embed_economy.add_field(name=f"📝 DEPOSIT",
                                    value=f"`{self.bot.PREFIX}deposit <amount>` or `/deposit all` to deposit your money",
                                    inline=inline_economy)
            embed_economy.add_field(name=f"🤝 PAY",
                                    value=f"`{self.bot.PREFIX}pay <user> <amount>` to pay the user money",
                                    inline=inline_economy)
            embed_economy.add_field(name=f"🕵️ ROB",
                                    value=f"`{self.bot.PREFIX}rob <user>` to steal money from the user",
                                    inline=inline_economy)
            embed_economy.add_field(name='🪙 COINFLIP',
                                    value=f'`{self.bot.PREFIX}flip <amount> <h / t>`, to flip a coin')
            embed_economy.add_field(name=f"🎲 GAMBLE", value=f"`{self.bot.PREFIX}gamble <amount>` to gamble with money",
                                    inline=inline_economy)
            await ctx.send(embed=embed_economy)

        elif help_type == "mod":
            embed_mod = Embed(title="HELP MENU", description='for help_typeration', color=Color.random())
            inline_mod = False
            Bot_owner_role = utils.get(ctx.guild.roles, id=settings['roles']['bot_owner'])
            embed_mod.add_field(name='🧹 clear', value=f"`{self.bot.PREFIX}clear (amount)` to clear message",
                                inline=inline_mod)
            embed_mod.add_field(name='🔇 mute', value=f"`{self.bot.PREFIX}mute <user>` to clear message",
                                inline=inline_mod)
            embed_mod.add_field(name='🔈 unmute', value=f"`{self.bot.PREFIX}unmute <user>` to clear message",
                                inline=inline_mod)
            embed_mod.add_field(name='⚠️ warn', value=f"`{self.bot.PREFIX}warn <user>` to clear message",
                                inline=inline_mod)
            embed_mod.add_field(name='🛑 stop',
                                value=f"`{self.bot.PREFIX}shutdown` to stop the bot (can be only user by {Bot_owner_role.mention})",
                                inline=inline_mod)
            embed_mod.add_field(name='🕰️ Time',
                                value=f'`{self.bot.PREFIX}time` to see this time (this can be used by everyone)')
            embed_mod.set_footer(text='these commands can only be done by a Trusted Staff or above')
            await ctx.send(embed=embed_mod)

        elif help_type == "level":
            inline_level = False
            embed_level = Embed(title='HELP MENU', description='for level', color=Color.random())
            embed_level.add_field(name='Level', value=f'`{self.bot.PREFIX}level (user)` to see your/user\'s level',
                                  inline=inline_level)
            embed_level.add_field(name='Rank',
                                  value=f'`{self.bot.PREFIX}rank (user)`, working on to make this on a card...',
                                  inline=inline_level)
            embed_level.add_field(name='Leaderboard',
                                  value=f'`{self.bot.PREFIX}lb`, to see this leaderboard of levels.')
            await ctx.send(embed=embed_level)

        else:
            helpme = self.bot.get_emoji(settings['emojis']['help_me'])
            embed_error = Embed(title=f"HELP MENU", color=Color.random())
            embed_error.add_field(name=f'ERROR', value=f'category not available {helpme}')
            embed_error.add_field(name=f'Still need help ?',
                                  value=f'DM me and I will try to reply as soon as possible :smile:',
                                  inline=False)
            await ctx.send(embed=embed_error)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")


def setup(bot):
    bot.add_cog(Help(bot))
