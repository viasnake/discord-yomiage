import json
import logging
import os
import platform
import random
import sys

import discord
from discord.ext import tasks
from discord.ext.commands import Bot, Context

# Check if the config file exists
if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/config.json"):
    sys.exit("'config.json' not found.")
else:
    with open(f"{os.path.realpath(os.path.dirname(__file__))}/config.json") as file:
        config = json.load(file)

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True


#
class LoggingFormatter(logging.Formatter):

    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"

    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    # Log colors
    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    #
    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = "(black){asctime}(reset) (levelcolor){levelname:<8}(reset) (green){name}(reset) {message}"
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


# Initialize the logger
logger = logging.getLogger("yomiage")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(LoggingFormatter())

# File handler
file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
file_handler_formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
)
file_handler.setFormatter(file_handler_formatter)

# Add the handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)


#
class Bot(commands.Bot):

    #
    def __init__(self):

        # Initialize the bot
        super().__init__(
            command_prefix=config["prefix"],
            description=config["description"],
            intents=intents,
        )
        self.logger = logger
        self.config = config

    #
    async def setup_hook(self) -> None:

        # Output the bot information
        self.logger.info("Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")

        # Load the cogs
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
                    self.load_extension(f"cogs.{extension}")
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
        if context.guild is None:
            self.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
            )

        # Log the command. But why is this here?
        self.logger.error("This should not have happened.")
        self.logger.info(f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")

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
        await self.change_presence(activity=discord.Game(name=random.choice(config["status"])))

    #
    @status_task.before_loop
    async def before_status_task(self) -> None:

        # Wait until the bot is ready
        await self.wait_until_ready()


# Initialize the bot
bot = Bot()
bot.run(config["token"])
