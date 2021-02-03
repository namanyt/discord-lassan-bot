from datetime import datetime
from json import load

from discord import Embed, Color
from discord.ext.commands import Cog, command, cooldown, BucketType


class Shop(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("shop")

    @command(name='shop')
    @cooldown(1, 2, type=BucketType.user)
    async def shop_command(self, ctx, category: str = None):
        inline = False
        with open("./data/json/shop.json", "r") as f:
            shop_json = load(f)

        shop_embed = Embed(title='SHOP',
                           timestamp=datetime.utcnow(),
                           color=Color.random())

        if category is None:
            for categories in shop_json:
                name = categories
                shop_embed.add_field(name=f'{name}', value=f'do `{self.bot.PREFIX}shop {name}`', inline=inline)

        else:
            for item in shop_json[category]:
                name = item['name']
                item_name = item['item_name']
                price = item['price']
                HTB = item['HowToBuy']
                HTS = item['HowToSell']

                shop_embed.add_field(name=f'{item_name}',
                                     value=f'Price: {price} \n '
                                           f'How To Buy: {HTB} \n '
                                           f'How To Sell: {HTS}',
                                     inline=inline)
        await ctx.send(embed=shop_embed)


def setup(bot):
    bot.add_cog(Shop(bot))
