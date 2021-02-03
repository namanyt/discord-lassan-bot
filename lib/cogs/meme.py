from requests import get
from discord import Embed
from discord.ext.commands import Cog, command


class Meme(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='meme')
    async def meme_maker_and_sender(self, ctx):
        r = get("https://memes.blademaker.tv/api/dankmemes")
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
        meme_embed = Embed(title=title)
        meme_embed.set_image(url=image)
        meme_embed.set_footer(text=f'👍:{UpVotes} 👎:{DownVote}')
        await ctx.send(embed=meme_embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('meme')


def setup(bot):
    bot.add_cog(Meme(bot))
