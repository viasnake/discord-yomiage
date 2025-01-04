from discord.ext import commands
from discord.ext.commands import Bot, Context # type: ignore
from logger import Logger


#
class Sync(commands.Cog, name="sync"):

    #
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.logger = Logger("sync cog")

    #
    @commands.hybrid_command(
        name="sync",
        description="Sync slash commands.",
    )
    @commands.is_owner()
    async def sync(self, context: Context, scope: str = "guild") -> None:

        #
        if scope == "global":
            self.logger.info("Syncing commands globally...")
            await context.bot.tree.sync()
            await context.send("Commands synced globally.")
            return

        #
        self.logger.info("Syncing commands in guild...")
        await context.bot.tree.sync(guild=context.guild)
        await context.send("Commands synced in guild.")


#
async def setup(bot: Bot) -> None:
    await bot.add_cog(Sync(bot))
