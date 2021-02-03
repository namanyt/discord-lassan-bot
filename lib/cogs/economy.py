from datetime import datetime
from json import dump, load
from random import randint, randrange, choice

from discord import Member, Embed, Color
from discord.ext.commands import Cog
from discord.ext.commands import command, Greedy, cooldown, BucketType


class Economy(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_bank_data(self):
        with open("./data/json/bank.json", "r") as f:
            users = load(f)
        return users

    async def open_account(self, user: Greedy[Member]):
        users = await self.get_bank_data()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["name"] = user.display_name
            users[str(user.id)]["wallet"] = 100
            users[str(user.id)]["bank"] = 0

        with open("./data/json/bank.json", "w") as f:
            dump(users, f)
        return True

    async def update_bank(self, user: Greedy[Member], change=0, mode='wallet'):
        users = await self.get_bank_data()
        users[str(user.id)][mode] += change

        with open("./data/json/bank.json", "w") as f:
            dump(users, f)

        bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
        return bal

    @command(name='bal', alieases=['balance', 'coins', 'coin', 'bank'])
    @cooldown(1, 2, BucketType.user)
    async def account_balance(self, ctx, target: Member = None):
        if not target:
            await self.open_account(ctx.author)
            user = ctx.author
            users = await self.get_bank_data()

            wallet_amt = users[str(user.id)]["wallet"]
            bank_amt = users[str(user.id)]["bank"]

            em = Embed(title=f"{ctx.author.name}'s balance", colour=Color.random())
            em.add_field(name='wallet', value=wallet_amt)
            em.add_field(name='bank', value=bank_amt)
            await ctx.send(embed=em)

        else:
            await self.open_account(target)
            user = target
            users = await self.get_bank_data()

            wallet_amt = users[str(user.id)]["wallet"]
            bank_amt = users[str(user.id)]["bank"]

            em = Embed(title=f"{ctx.author.name}'s balance", colour=Color.random())
            em.add_field(name='wallet', value=wallet_amt)
            em.add_field(name='bank', value=bank_amt)
            await ctx.send(embed=em)

    @command(name='daily', aliases=['d'])
    @cooldown(1, 2, BucketType.user)
    async def daily(self, ctx):
        await self.open_account(ctx.author)
        users = await self.get_bank_data()
        user = ctx.author
        daily_reward = 100
        daily_embed = Embed(title="🎉 Daily Reward 🎉")
        daily_embed.add_field(name='Here u go guy...', value=f'Your {daily_reward} as daily reward !')
        await ctx.send(embed=daily_embed)
        users[str(user.id)]["wallet"] += daily_reward
        with open("./data/json/bank.json", "w") as f:
            dump(users, f)
        return True

    @command(name='beg')
    @cooldown(1, 2, BucketType.user)
    async def begging(self, ctx):
        await self.open_account(ctx.author)
        users = await self.get_bank_data()
        user = ctx.author
        earnings = randrange(101)

        beg_embed = Embed(color=Color.random())
        beg_embed.add_field(name="BEG", value=f'Someone gave you ${earnings} !!')

        await ctx.send(embed=beg_embed)

        users[str(user.id)]["wallet"] += earnings

        with open("./data/json/bank.json", "w") as f:
            dump(users, f)
        return True

    @command(name='deposit', aliases=['dep'])
    @cooldown(1, 2, BucketType.user)
    async def deposit(self, ctx, amount=None):
        await self.open_account(ctx.author)
        bal = await self.update_bank(ctx.author)
        wallet = bal[0]

        if not amount:
            await ctx.send("Please enter the amount")
            return

        if bal[0] > 0:
            if amount == "max" or amount == "all":
                await self.update_bank(ctx.author, wallet * -1)
                await self.update_bank(ctx.author, wallet, "bank")
                await ctx.send(f"Successfully deposited {bal[0]}.")
                return

        amount = int(amount)

        if amount > bal[0]:
            await ctx.send("You don't have enough money")
            return
        if amount < 0:
            await ctx.send("Amount must be a positive number")
            return
        await self.update_bank(ctx.author, amount * -1)
        await self.update_bank(ctx.author, amount, "bank")

        await ctx.send(f"Successfully deposited {amount}.")

    @command(name='withdraw', aliases=['with'])
    @cooldown(1, 2, BucketType.user)
    async def withdraw(self, ctx, amount=None):
        await self.open_account(ctx.author)
        bal = await self.update_bank(ctx.author)
        wallet = bal[1]

        if not amount:
            await ctx.send("Please enter the amount")
            return

        if bal[1] > 0:
            if amount == "max" or amount == "all":
                await self.update_bank(ctx.author, wallet)
                await self.update_bank(ctx.author, -1 * wallet, "bank")
                await ctx.send(f"Successfully withdrew {bal[1]}.")
                return

        amount = int(amount)

        if amount > bal[1]:
            await ctx.send("You don't have enough money")
            return
        if amount < 0:
            await ctx.send("Amount must be a positive number")
            return
        await self.update_bank(ctx.author, amount)
        await self.update_bank(ctx.author, -1 * amount, "bank")

        await ctx.send(f"Successfully withdrew {amount}.")

    @command(name='pay', aliases=['give'])
    @cooldown(1, 2, BucketType.user)
    async def pay(self, ctx, member: Member, amount=None):
        await self.open_account(ctx.author)
        await self.open_account(member)

        if not amount:
            await ctx.send("Please enter the amount")
            return

        bal = await self.update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[0]:
            await ctx.send("You don't have enough money")
            return
        if amount < 0:
            await ctx.send("Amount must be a positive number")
            return
        await self.update_bank(ctx.author, -1 * amount, "wallet")
        await self.update_bank(member, amount, "wallet")

        await ctx.send(f"Successfully paid {amount}.")

    @command(name='rob', aliases=['steal'])
    @cooldown(1, 2, BucketType.user)
    async def rob(self, ctx, member: Member):
        await self.open_account(ctx.author)
        await self.open_account(member)

        bal = await self.update_bank(member)
        userBal = await self.update_bank(ctx.author)
        if bal[0] < 100:
            await ctx.send("They don't have enough money to ROB")
            return
        if userBal[0] < 100:
            await ctx.send("You don't gave enough money to rob")
            return

        amount = randint(-userBal[0], bal[0])

        if amount > 0:
            await self.update_bank(ctx.author, amount)
            await self.update_bank(member, -1 * amount)
            await ctx.send(f"Successfully robbed and got {amount}.")
        else:
            await self.update_bank(member, -1 * amount)
            await self.update_bank(ctx.author, amount)
            await ctx.send(f"They saw and took {amount}")

    @command(name='flip', aliases=['coinflip'])
    @cooldown(1, 2, BucketType.user)
    async def coin_flip(self, ctx, amount=None, face: str = None):
        await self.open_account(ctx.author)

        if amount is None:
            await ctx.send("Please Enter some amount to gamble...")
            return
        bal = await self.update_bank(ctx.author)
        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("You don't have enough money to gamble with")
            return
        if amount < 0:
            await ctx.send("Amount must not be below zero !")
            return

        if face is None:
            await ctx.send("Please Enter the coin face u want to gamble with (h / t) to gamble...")
            return

        diceiding_face = randint(0, 2)
        predicted_face = face

        answer_face = None
        if diceiding_face == 0:
            answer_face = "h"
        if diceiding_face == 1:
            answer_face = "t"

        if predicted_face == "h":
            if answer_face == predicted_face:
                win_em = Embed(title='You WON !', color=Color.random(), timestamp=datetime.utcnow())
                await ctx.send(embed=win_em)
                await self.update_bank(ctx.author, 2 * amount, "wallet")
            else:
                await self.update_bank(ctx.author, -1 * amount, "wallet")
                lose_em = Embed(title='You LOST !', color=Color.random(), timestamp=datetime.utcnow())
                await ctx.send(embed=lose_em)

        if predicted_face == "t":
            if answer_face == predicted_face:
                win_em = Embed(title='You WON !', color=Color.random(), timestamp=datetime.utcnow())
                await ctx.send(embed=win_em)
                await self.update_bank(ctx.author, 2 * amount, "wallet")
            else:
                await self.update_bank(ctx.author, -1 * amount, "wallet")
                lost_em = Embed(title='You LOST !', color=Color.random(), timestamp=datetime.utcnow())
                await ctx.send(embed=lost_em)

    @command(name='gamble')
    @cooldown(1, 2, BucketType.user)
    async def money_gamble(self, ctx, amount=None):
        await self.open_account(ctx.author)

        if amount is None:
            await ctx.send("Please Enter some amount to gamble...")
            return
        bal = await self.update_bank(ctx.author)
        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("You don't have enough money to gamble with")
            return
        if amount < 0:
            await ctx.send("Amount must not be below zero !")
            return

        final = []
        for i in range(4):
            a = choice(["A", "B", "C"])

            final.append(a)
            if i == 3:
                final2 = "| " + final[0] + " | " + final[1] + " | " + final[2] + " |"

        if final[0] == final[1] and final[0] == final[2] and final[1] == final[2]:
            await self.update_bank(ctx.author, 2 * amount, "wallet")
            embed = Embed(title="Lottery")
            embed.add_field(name=final2, value="You Win (0w0)", inline=False)
            await ctx.send(embed=embed)
        else:
            await self.update_bank(ctx.author, -1 * amount, "wallet")
            embed = Embed(title="Lottery")
            embed.add_field(name=final2, value="You Lost (;-;)", inline=False)
            await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("economy")


def setup(bot):
    bot.add_cog(Economy(bot))
