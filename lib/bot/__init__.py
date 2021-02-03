from asyncio import sleep
from json import load
from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import ActivityType, Status, Activity
from discord import Intents, Forbidden, NotFound
from discord.ext.commands import Bot as BotBase, Context, CommandOnCooldown, NotOwner
from discord.ext.commands import (CommandNotFound, BadArgument, MissingRequiredArgument)


with open('./lib/bot/settings.json', 'r') as f:
    settings = load(f)


PREFIX = settings['prefix']
OWNER_IDS = settings['owner_ids']
COGS = [p.stem for p in Path(".").glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = [CommandNotFound, BadArgument]

from ..db import db


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{str(cog).upper()} => READY")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.stdout = None
        self.VERSION = None
        self.TOKEN = None
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(scheduler=self.scheduler)

        super().__init__(command_prefix=PREFIX,
                         owner_ids=OWNER_IDS,
                         intents=Intents.all(),
                         case_insensitive=True)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{str(cog).upper()} => LOADED")

        print("> SETUP COMPLETED")

    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
                     ((guild.id,) for guild in self.guilds))

        db.multiexec("INSERT OR IGNORE INTO exp (UserID) VALUES (?)",
                     ((member.id,) for member in self.guild.members if not member.bot))

        to_remove = []
        stored_members = db.column("SELECT UserID FROM exp")
        for id_ in stored_members:
            if not self.guild.get_member(id_):
                to_remove.append(id_)

        db.multiexec("DELETE FROM exp WHERE UserID = ?",
                     ((id_,) for id_ in to_remove))

        db.commit()

    def run(self, version):
        self.VERSION = version

        print("> RUNNING SETUP")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        print(">> RUNNING BOT !")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.send("I'm not ready to receive commands.")
                await ctx.send("please wait")

    async def on_connect(self):
        print('CONNECTED')

    async def on_disconnected(self):
        print('DISCONNECTED')

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send('Something went wrong.')

        await self.stdout.send("An error has spawned")

        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send('This command might be in correct')

        elif isinstance(exc, CommandNotFound):
            await ctx.send('This command is not available in my database')

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("Command is incomplete")

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f"That command is on cooldown. try again in {exc.retry_after:,.2f} secs.")

        elif hasattr(exc, "original"):
            if isinstance(exc.original, Forbidden):
                await ctx.send("I dont have the permission to that...")

        elif isinstance(exc, NotOwner):
            await ctx.send("Sorry, you don't actually own this bot")

        elif isinstance(exc, NotFound):
            pass

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.stdout = self.get_channel(settings['channel']['stdout'])
            self.guild = self.get_guild((settings['guild']))
            self.scheduler.start()
            await self.change_presence(activity=Activity(type=ActivityType.streaming, name="bored... i'm AFK"),
                                       status=Status.dnd, afk=True)
            await self.stdout.send("Bonjour !")

            self.update_db()

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print("! ONLINE")
        else:
            print("! RECONNECTED")

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
