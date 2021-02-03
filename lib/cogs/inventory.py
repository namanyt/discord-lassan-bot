from json import load, dump

from discord import Color, Embed
from discord.ext.commands import Cog, command, cooldown, BucketType


class Inventory(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('inventory')

    async def make_inv(self, user):
        with open('./data/json/inv.json', 'r') as f:
            inv = load(f)

        if str(user.id) in inv:
            return False
        else:
            inv[str(user.id)] = {}
            inv[str(user.id)]['name'] = str(user)
            inv[str(user.id)]['inv'] = {}
            inv[str(user.id)]['inv']['item_name'] = []
            inv[str(user.id)]['inv']['item_id'] = []
            inv[str(user.id)]['inv']['item_desc'] = []

        with open('./data/json/inv.json', 'w') as f:
            dump(inv, f)
        return True

    @command(name='inv', aliases=['bag', 'inventory'])
    @cooldown(1, 2, BucketType.user)
    async def open_inv(self, ctx):
        user = ctx.author
        await self.make_inv(user=user)
        inventory_embed = Embed(title=f'{user.name}\'s Inventory',
                                color=Color.random())
        with open('./data/json/inv.json', 'r') as f:
            inv = load(f)

        with open('./data/json/shop.json', 'r') as f:
            shop = load(f)

        for item_name in inv[str(user.id)]['inv']['item_name']:
            for item_id in inv[str(user.id)]['inv']['item_id']:
                if str(item_name).lower() == str(item_id).lower():
                    inventory_embed.add_field(name=f'{item_name}', value=f'*ID* --> {item_id}', inline=False)
                else:
                    pass

        await ctx.send(embed=inventory_embed)


def setup(bot):
    bot.add_cog(Inventory(bot))
