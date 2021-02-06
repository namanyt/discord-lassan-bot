from asyncio import TimeoutError, sleep
from datetime import datetime
from random import choice

from discord import Embed, TextChannel
from discord.ext.commands import Cog, command

from lib.bot import settings


def convert(time):
    pos = ['s', 'm', 'h', 'd']
    time_dict = {"s": 1, 'm': 60, "h": 3600, "d": 3600 * 24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]


class Giveaway(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='gcreate')
    async def create_giveaway(self, ctx):
        await ctx.send("Let's start with this giveaway! \n Answer these questions withing 15 seconds.")

        questions = ['Which channel should it be hosted in?',
                     'What should be the duration of the giveaway (s|m|h|d)',
                     'What is the prize of the giveaway?']

        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            except TimeoutError:
                await ctx.send('You didn\'t answer in time, please try again quicker')
                return
            else:
                answers.append(msg.content)

        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"Please try again and mention a channel properly.")
            await ctx.send(f"eg: <#784374747566964747>")
            return

        channel = self.bot.get_channel(c_id)

        time = convert(answers[1])
        if time == -1:
            await ctx.send('You did not mention the time properly.')
            await ctx.send('eg: use (s|m|h|d) after the time \n `10s`')
            return
        elif time == -2:
            await ctx.send('The time must be a number !')
            return

        prize = answers[2]

        await ctx.send(f"The Giveaway will be ot hosted in {channel.mention} and will loast for {answers[1]} !")

        g_embed = Embed(title='🎉 GIVEAWAY 🎉',
                        description=f'Hosted by: {ctx.author.mention}',
                        timestamp=datetime.utcnow())

        g_embed.add_field(name=f"Prize:", value=f"{prize}")
        g_embed.set_footer(text=f"Ends {answers[1]} from now")

        giveaway = await channel.send(embed=g_embed)
        await giveaway.add_reaction("🎉")
        await sleep(time)
        new_msg = await channel.fetch_message(giveaway.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        winner = choice(users)
        await channel.send(f"Congratulations ! {winner.mention} won {prize}")
        g_winner = Embed(title='🎉 GIVEAWAY ENDED 🎉', timestamp=datetime.utcnow())
        g_winner.add_field(name=f"Winner: {winner}", value=f"Prize: {prize}")
        await giveaway.edit(embed=g_winner)

    @command(name='gstart')
    async def start_giveaway(self, ctx, time=None, channel: TextChannel = None, *, prize: str = None):
        giveaway_time = convert(time)
        giveaway_channel = channel
        if channel is None:
            giveaway_channel = self.bot.get_channel(settings['channel']['giveaway'])
        elif time is None:
            await ctx.send('please mention the time.\n eg:`1s`, `10m`, `12h`, `3d`')
            return
        elif prize is None:
            await ctx.send('please also send the name of the prize')
            return
        elif giveaway_time == -1:
            await ctx.send('You did not mention the time properly.')
            await ctx.send('eg: use (s|m|h|d) after the time \n `10s`')
            return
        elif giveaway_time == -2:
            await ctx.send('The time must be a number !')
            return
        await ctx.send(f"Stat giveaway for {prize} till {time}")
        g_embed = Embed(title='🎉 GIVEAWAY 🎉',
                        description=f'Hosted by: {ctx.author.mention}',
                        timestamp=datetime.utcnow())

        g_embed.add_field(name=f"Prize:", value=f"{prize}")
        g_embed.set_footer(text=f"Ends {time} from now")

        giveaway = await giveaway_channel.send(embed=g_embed)
        await giveaway.add_reaction("🎉")
        await sleep(giveaway_time)
        new_msg = await channel.fetch_message(giveaway.id)
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        winner = choice(users)
        await giveaway_channel.send(f"Congratulations ! {winner.mention} won {prize}")
        g_winner = Embed(title='🎉 GIVEAWAY ENDED 🎉', timestamp=datetime.utcnow())
        g_winner.add_field(name=f"Winner: {winner}", value=f"Prize: {prize}")
        await giveaway.edit(embed=g_winner)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("giveaway")


def setup(bot):
    bot.add_cog(Giveaway(bot))
