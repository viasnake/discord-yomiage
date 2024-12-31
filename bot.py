import os
import platform
import random

from config import ConfigLoader
from logger import Logger

import discord
from discord.ext import tasks
from discord.ext.commands import Bot, Context


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
        super().__init__(
            command_prefix=self.config.get("prefix"),
            intents=intents,
        )

    #
    async def setup_hook(self) -> None:

        # Log the bot information
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")

        #
        await self.load_cogs()

        # Start the status task
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
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])

        # Log the command in a guild
        if context.guild is not None:
            self.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
            )

        # Log the command in DMs
        else:
            self.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
            )

    #
    async def on_command_error(self, context: Context, exception: Exception) -> None:

        # Log the exception
        self.logger.error(f"Ignoring exception in command {context.command}:", exc_info=exception)

    #
    async def on_message(self, message: discord.Message) -> None:

        # Ignore messages sent by the bot
        if message.author.bot:
            return

        # Ignore messages sent by self
        if message.author.id == self.user.id:
            return

        # Process the commands
        await self.process_commands(message)

    #
    @tasks.loop(seconds=60)
    async def status_task(self) -> None:

        # Set the status
        await self.change_presence(
            activity=discord.Game(
                name=random.choice(self.config.get("status"))
            )
        )

    #
    @status_task.before_loop
    async def before_status_task(self) -> None:

        # Wait until the bot is ready
        await self.wait_until_ready()

#
config = ConfigLoader()

#
Discord().run(config.get("token"))
