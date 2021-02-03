from asyncio import sleep
from random import choice, randint

from discord import Embed, Member, Color
from discord.ext.commands import Cog, command, Greedy, cooldown, BucketType


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='hello')
    async def say_hi(self, ctx):
        await ctx.send(f"{str(choice(['hello', 'hi', 'hey', 'What sup'])).upper()} {ctx.author.display_name}!")

    @command(name='kill')
    async def kill_user(self, ctx, user: Greedy[Member] = None):
        kill_log = [f'"{ctx.author.display_name}" took "{user.display_name}\'s" balls out. wtf',
                    f'"{ctx.author.display_name}" roasted "{user.display_name}"',
                    f'"{user.display_name}" fell out of the world (WTF ?!)',
                    f'"{user.display_name}" fell down a cliff while playing Pokemon Go. Good job on keeping your nose in that puny phone.',
                    f'"{user.display_name}" takes an arrow to the knee. And everywhere else.',
                    f'"{user.display_name}" drowned in their own tears.']

        if not user or user == self.bot.user:
            em = Embed(title='You cannot kill me !', color=Color.random())
            em.set_image(url="https://i.kym-cdn.com/photos/images/newsfeed/001/488/935/c09.jpg")
            await ctx.send(embed=em)
            return
        if user == ctx.author:
            await ctx.send("DO NOT")
            await ctx.send("DO")
            await ctx.send("IT!!")
            return
        else:
            kill_feed = choice(kill_log)
            await ctx.send(f"{kill_feed}")
            return

    @command(name='lenny')
    @cooldown(1, 2, type=BucketType.user)
    async def lenny_command_face(self, ctx):
        await ctx.send('( ͡° ͜ʖ ͡°)')
        return

    @command(name='cute')
    @cooldown(1, 2, type=BucketType.user)
    async def cute_command_face(self, ctx):
        await ctx.send('(っ◔◡◔)っ')
        return

    @command(name='doot')
    @cooldown(1, 2, type=BucketType.user)
    async def doot_mock_text(self, ctx, *, message: str = None):
        if message == None:
            await ctx.send('what the hell u want me to say !')
            return
        LIST = message.split(' ')
        await ctx.send(" \💀\🎺 ".join(LIST))
        return

    @command(name='dankrate')
    @cooldown(1, 2, type=BucketType.user)
    async def dankrate_machine(self, ctx):
        dank_rate_percentage = randint(0, 100)
        await ctx.send(f'you are {dank_rate_percentage}% danky boi')

    @command(name='hack')
    @cooldown(1, 2, type=BucketType.user)
    async def fake_hack(self, ctx, target: Member = None, virus_name=None):
        if target is None:
            await ctx.send('who should i hack...')
            return
        if virus_name is None:
            virus_name = 'trojan'
        repeat = 0
        message = await ctx.send(
            f"OK ! {ctx.author.display_name}, it is time to \ndo a totally real and powerful hack on {target.display_name}")
        await sleep(2)
        while repeat <= 2:
            await message.edit(content=".")
            await sleep(0.1)
            await message.edit(content='..')
            await sleep(0.1)
            await message.edit(content='...')
            repeat += 1
        repeat = 0
        await sleep(0.1)
        await message.edit(content=f'entered the data base of {target.display_name}')
        await sleep(1.5)
        await message.edit(content=f'injecting {virus_name} virus...')
        await sleep(2)
        while repeat <= 2:
            await message.edit(content='and.')
            await sleep(0.1)
            await message.edit(content='and..')
            await sleep(0.1)
            await message.edit(content='and...')
            repeat += 1
        await sleep(1)
        await message.edit(content='A totally real hack us done !')

    @command(name='say')
    @cooldown(1, 2, type=BucketType.user)
    async def say_message(self, ctx, *, message: str = None):
        if message is None:
            await ctx.send('what should i say ??')
            return
        await ctx.send(f'{message} \n \n**{ctx.author}**')
        return

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")


def setup(bot):
    bot.add_cog(Fun(bot))
