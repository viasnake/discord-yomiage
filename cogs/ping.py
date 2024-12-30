import discord
from discord.ext import commands
from discord.ext.commands import Context


#
class Ping(commands.Cog, name="ping"):

    #
    def __init__(self, bot):
        self.bot = bot

    #
    @commands.hybrid_command(
        name="ping",
        description="Show the bot's latency.",
    )
    async def ping(self, context: Context) -> None:

        #
        await context.send(f"Pong! {round(self.bot.latency * 1000)}ms")


async def setup(bot):
    await bot.add_cog(Ping(bot))
