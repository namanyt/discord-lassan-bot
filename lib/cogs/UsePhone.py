from asyncio import sleep
from json import load
from random import choice

from discord import Embed
from discord.ext.commands import Cog, command
from requests import get


class UsePhone(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('UsePhone')

    @command(name='reddit')
    async def scroll_reddit(self, ctx, subreddit: str = None):
        user = ctx.author

        with open('./data/json/inv.json', 'r') as f:
            phone = load(f)

        if "phone" in phone[str(user)]['inv']['item_id']:

            if subreddit is None:
                subreddit = 'dankmemes'

            r = get(f"https://memes.blademaker.tv/api/{subreddit}")
            res = r.json()
            title = res['title']
            image = res['image']
            sub = res['subreddit']
            UpVotes = res['ups']
            DownVote = res['downs']
            nsfw = res['nsfw']

            if nsfw:
                await ctx.send('meme is nsfw')
                return
            meme_embed = Embed(title=title, description=f'from {sub}')
            meme_embed.set_image(url=image)
            meme_embed.set_footer(text=f'👍:{UpVotes} 👎:{DownVote}')
            await ctx.send(embed=meme_embed)

        else:
            await ctx.send('you don\'t a phone.')

    @command(name='call')
    async def phone_call(self, ctx, who=None):
        user = ctx.author

        with open('./data/json/inv.json', 'r') as f:
            phone = load(f)

        if "phone" in phone[str(user)]['inv']['item_id']:

            if who is None:
                msg = ('who do u wanna call ? \n'
                       f'1. **Police** (if there is an emergency) `{self.bot.PREFIX}call police`\n'
                       f'2. **My developers** (for updates and sneak peeks) `{self.bot.PREFIX}call dev`\n'
                       f'3. **Prank Call someone** (name is the description) `{self.bot.PREFIX}call prank`\n'
                       'more will be added l8r !')

                await ctx.send(msg)

            who = who.lower()

            if who == 'police':
                emergency = choice(['cat has climbed my tree',
                                    "i'm being kidnapped !",
                                    'my house is on fire !',
                                    'there are burglars at my house'])
                await ctx.send('Hello? This is **911**, what is your emergency ?')
                await sleep(.5)
                await ctx.send(emergency)
                await sleep(.5)
                await ctx.send('np problem gays, we are heading to you **ASAP**')
                await ctx.send('`CALL DISCONNECTED`')
                return

            elif who == "dev":
                updates = choice(['NO',
                                  'nah',
                                  'stickers boiii',
                                  'FREE NITRO',
                                  'SELF GIVEAWAYS'])
                await ctx.send(f'**YOU** Hello ?')
                await ctx.send(f'**DEV** Hi ?')
                await sleep(0.5)
                await ctx.send('**YOU** Are you adding any new updates ?')
                await sleep(0.5)
                await ctx.send(f'**DEV** {updates} updates !!!!')
                await sleep(0.5)
                await ctx.send('**YOU** cool')
                await sleep(0.5)
                await ctx.send('`CALL DISCONNECTED`')
                return

            elif who == "prank":
                pass

            else:
                pass
        else:
            await ctx.send('you don\'t own a phone.')


def setup(bot):
    bot.add_cog(UsePhone(bot))
