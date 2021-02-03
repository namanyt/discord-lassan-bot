from json import load, dump

from discord.ext.commands import Cog, command, cooldown, BucketType


class Sell(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='sell')
    @cooldown(1, 2, type=BucketType.user)
    async def sell_item(self, ctx, category, item_user):
        user = ctx.author
        with open('./data/json/shop.json', 'r') as f:
            shop = load(f)

        with open('./data/json/inv.json', 'r') as f:
            inv = load(f)

        with open('./data/json/bank.json', 'r') as f:
            bank = load(f)

        if category in shop:
            for items in shop[category]:
                price = items['price']
                item_name = items['item_name']
                item_id = items['name']
                item_desc = items['desc.']
                if item_user in item_id:
                    if item_user in inv[str(user.id)]['inv']['item_id']:
                        inv[str(user.id)]['inv']['item_name'].remove(item_name)
                        inv[str(user.id)]['inv']['item_id'].remove(item_id)
                        inv[str(user.id)]['inv']['item_desc'].remove(item_desc)
                        bank[str(user.id)]['wallet'] += (price//2)
                        await ctx.send(f'{item_name} sold successfully')

                        with open('./data/json/bank.json', 'w') as f:
                            dump(bank, f)

                        with open('./data/json/inv.json', 'w') as f:
                            dump(inv, f)

                        return

                    else:
                        await ctx.send(f'{item_name} is not in your inventory')
                        return
        else:
            await ctx.send(f'{item_user} not available in store')
            return

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('sell')


def setup(bot):
    bot.add_cog(Sell(bot))
