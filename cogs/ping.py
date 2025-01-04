from discord.ext import commands
from discord.ext.commands import Bot, Context # type: ignore
from logger import Logger

#
class Ping(commands.Cog, name="ping"):

    #
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.logger = Logger("ping cog")

    #
    @commands.hybrid_command(
        name="ping",
        description="Show the bot's latency.",
    )
    async def ping(self, context: Context) -> None:
        await context.send(f"Pong! {round(self.bot.latency * 1000)}ms")


#
async def setup(bot: Bot) -> None:
    await bot.add_cog(Ping(bot))
