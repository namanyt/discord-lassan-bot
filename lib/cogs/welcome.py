from io import BytesIO
from os import remove
from time import sleep

from PIL import Image, ImageFont, ImageDraw, ImageOps
from discord import Forbidden, Member, File, Embed
from discord.ext.commands import Cog, command
from requests import get

from ..bot import settings
from ..db import db


def get_name(text, color=(255, 255, 255, 255)):
    name = text.display_name
    font = ImageFont.truetype('lib/utils/font.ttf', 75)
    txt = Image.new("RGBA", font.getsize(name), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(txt)
    draw.text((0, 0), name, align='center', font=font, fill=color)
    return txt


def get_icon(name: Member):
    size = (300, 300)
    im = Image.open(BytesIO(get(name.avatar_url).content))
    im.save('pfp.png')
    sleep(2)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0)+size, fill=255)
    with Image.open('pfp.png') as f:
        out = ImageOps.fit(f.convert("RGBA"), mask.size, centering=(0.5, 0.5))
        out.putalpha(mask)
    return out


def get_server_details(text, color=(100, 100, 100, 255)):
    font = ImageFont.truetype('lib/utils/font.ttf', 30)
    txt = Image.new("RGBA", font.getsize(text), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(txt)
    draw.text((0, 0), text, font=font, fill=color)
    return txt


def get_server_details2(text, color=(100, 100, 100, 255)):
    font = ImageFont.truetype('lib/utils/font.ttf', 20)
    txt = Image.new("RGBA", font.getsize(text), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(txt)
    draw.text((0, 0), text, font=font, fill=color)
    return txt


def create_welcome_card(name: Member):
    base = Image.new("RGBA", (1000, 700), color=(28, 28, 28, 255))
    base2 = Image.new("RGBA", (900, 600), color=(0, 0, 0, 255))

    base.alpha_composite(base2, (50, 50))

    # user
    base.alpha_composite(get_name(name), (348, 170))
    base.alpha_composite(get_icon(name), (60, 200))

    # server
    base.alpha_composite(get_server_details('Welcome to Lassan Gang'), (430, 370))
    base.alpha_composite(get_server_details2('Go ahead to #general and chat with others !'), (400, 430))

    base.save('welcome.png')
    return base


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("welcome")

    @command(name='welcome')
    async def test(self, ctx):
        name = ctx.author
        card = create_welcome_card(name)
        file = File("welcome.png")
        e = Embed(description=f"Welcome {ctx.author.mention} to TTUS")
        e.set_image(url="attachment://welcome.png")
        await ctx.send(file=file, embed=e)
        sleep(3)
        remove("welcome.png")

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
        name = member
        card = create_welcome_card(name)
        file = File("welcome.png")
        e = Embed(description=f"Welcome to **{member.guild.name}** {member.mention}! Head over to <#626608699942764548> to say hi!")
        e.set_image(url="attachment://welcome.png")
        await self.bot.get_channel(settings['channel']['welcome']).send(file=file, embed=e)
        try:
            await member.send(f"Welcome to **{member.guild.name}**! Enjoy your stay!")

        except Forbidden:
            pass

        await member.add_roles(member.guild.get_role(settings['roles']['friend']))

    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute("DELETE FROM exp WHERE UserID = ?", member.id)
        await self.bot.get_channel(settings['channel']['goodbye']).send(f"{member.display_name} has left {member.guild.name}.")


def setup(bot):
    bot.add_cog(Welcome(bot))
