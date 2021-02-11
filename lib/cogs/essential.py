from datetime import datetime

from discord import Embed, Color
from discord.ext.commands import Cog
from discord.ext.commands import command, cooldown, BucketType, is_owner
from pytz import timezone


class Essentials(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='time')
    @cooldown(1, 2, BucketType.user)
    async def time(self, ctx):
        tz = timezone('Asia/Kolkata')
        india_current_time = datetime.now(tz).strftime("%H:%M:%S %p")
        time_embed = Embed(title='Time', color=Color.random())
        time_embed.add_field(name=f"time is -->", value=india_current_time)
        await ctx.send(embed=time_embed)

    @is_owner()
    @command(name='rule')
    async def send_rules(self, ctx):
        rule_embed = Embed(title='__***RULES***__', timestamp=datetime.utcnow(), colour=Color.red())
        rules = [("** **\n***NO SPAM***",
                  "Don't spam. (Spamming includes song lyrics, zalgo, excessive caps/reaction spams, copy pastes, picture/link/GIF spam, reaction spam and walls of text)"),
                 ("** **\n***NO NSFW***",
                  "Don't post NSFW/Gore/18+ stuff in the channels. (Not only you shouldn't do this but, you also shouldn't \have any NSFW/Gore-ish Pfps/Nickname/Usernames"),
                 ("** **\n***NO HARRASSMENT***",
                  "Don't harass or insult any other members. (This includes threats, internet attacks and cyber bullying. Other people have feelings too.)"),
                 ("** **\n***DON'T EVADE PUNISHMENTS***",
                  "Don't try to evade punishments or mutes. (It won't work, trust me. Plus, you'll get instant-banned with no hesitation nor appeal.)"),
                 ("** **\n***NO ADVERTISING***",
                  "Don't advertise other Discord servers or Youtube videos, unless if allowed by a Staff. (Only advertise social media links in channels that allow advertisement. No discord links whatsoever.)"),
                 ("** **\n***NO IMPERSONATION***",
                  "Don't impersonate anyone, like YouTubers or Staff. (This includes copying avatars, nicknames, or just trolling to imitate an user)"),
                 ("** **\n***DON'T SWEAR/ABUSE***",
                  "Swearing is not allowed. (If someone is going all out on personal insults, a tirade of swear words,, they will be punished.)"),
                 ("** **\n***ABOUT CHAT***",
                  "Don't go off topic in any of the channels.  (Please keep within the designated topic of the channel.)"),
                 ("** **\n***ABOUT VOICE CHAT***",
                  "Don't be an annoyance in voice channels.  (This includes putting inappropriate songs unless the members won't disagree & earrape and shouting)"),
                 ("** **\n***BAN***", "We Don’t reveal the reason for your ban."),
                 ("** **\n***PERSONAL FIGHTS***",
                  "This server is not at all responsible for your personal fights so pls don't complain to us regarding your own personal matters."),
                 ("** **\n***RESPECT GIRLS***",
                  "Respect all the Girls if we found that you are doing any kind of Harassment in this server against Girls you will directly get banned from this server."),
                 ("** **\n***NO USING VOICEMOD***", "Use of voice mod may get you banned here."),
                 ]
        for name, value in rules:
            rule_embed.add_field(name=name, value=value, inline=False)

        await ctx.send(embed=rule_embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("essentials")


def setup(bot):
    bot.add_cog(Essentials(bot))