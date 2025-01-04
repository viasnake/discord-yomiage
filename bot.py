import os
import platform
import random

from config import ConfigLoader
from database import D1
from logger import Logger

import discord
from discord.ext import tasks
from discord.ext.commands import Bot, Context # type: ignore


#
class Discord(Bot):

    #
    def __init__(self):

        #
        intents = discord.Intents.default()
        intents.message_content = True

        #
        self.logger = Logger("Discord")
        self.config = ConfigLoader()

        #
        self.database = D1()

        #
        super().__init__(
            command_prefix=self.config.get("prefix"),
            intents=intents,
        )

    #
    async def setup_hook(self) -> None:

        #
        if self.user is not None:
            self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")

        #
        self.database.init_database()
        await self.load_cogs()
        self.status_task.start()

    #
    async def load_cogs(self) -> None:

        # Load the cogs
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):

            # Check if the file is a Python file
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    self.logger.info(f"Loaded extension '{extension}'")
                except Exception as e:
                    exception = f"{type(e).__name__}: {e}"
                    self.logger.error(f"Failed to load extension {extension}\n{exception}")

    #
    async def on_command_completion(self, context: Context) -> None:

        # Get the executed command
        if context.command is not None:
            full_command_name: str = context.command.qualified_name
            split: list[str] = full_command_name.split(" ")
            executed_command: str = split[0]
        else:
            executed_command: str = "Unknown"

        # Log the command in a guild
        if context.guild is not None:
            self.logger.info(f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")

        # Log the command in DMs
        else:
            self.logger.info(f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")

    #
    async def on_command_error(self, context: Context[Bot], exception: Exception) -> None:

        #
        self.logger.error(f"An exception occurred: {exception}")

    #
    async def on_message(self, message: discord.Message) -> None:

        # Ignore messages sent by the bot
        if message.author.bot:
            return

        # Ignore messages sent by self
        if self.user is not None and message.author.id == self.user.id:
            return

        # Process the commands
        await self.process_commands(message)

    #
    @tasks.loop(seconds=60)
    async def status_task(self) -> None:

        #
        status: str = random.choice(self.config.get("status"))
        await self.change_presence(activity=discord.Game(name=status))

    #
    @status_task.before_loop
    async def before_status_task(self) -> None:

        #
        await self.wait_until_ready()

#
config = ConfigLoader()

#
Discord().run(config.get("discord_token"))
