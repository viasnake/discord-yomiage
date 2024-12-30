from discord.ext import commands
from discord.ext.commands import Context


#
class Sync(commands.Cog, name="Sync"):

    #
    def __init__(self, bot):
        self.bot = bot

    #
    @commands.hybrid_command(
        name="sync",
        description="Sync slash commands.",
    )
    @commands.is_owner()
    async def sync(self, context: Context, scope: str = "guild") -> None:

        #
        if scope == "guild":
            self.bot.logger.info("Syncing commands in guild...")
            await self.bot.tree.sync(guild=context.guild)
            await context.send("Commands synced in guild.")
            return

        #
        if scope == "global":
            self.bot.logger.info("Syncing commands globally...")
            await self.bot.tree.sync()
            await context.send("Commands synced globally.")
            return

        #
        await context.send("Invalid scope.")

    #
    @commands.hybrid_command(
        name="unsync",
        description="Unsync slash commands.",
    )
    @commands.is_owner()
    async def unsync(self, context: Context, scope: str = "guild") -> None:

        #
        if scope == "guild":
            self.bot.logger.info("Unsyncing commands in guild...")
            await self.bot.tree.unsync(guild=context.guild)
            await context.send("Commands unsynced in guild.")
            return

        #
        if scope == "global":
            self.bot.logger.info("Unsyncing commands globally...")
            await self.bot.tree.unsync()
            await context.send("Commands unsynced globally.")
            return

        #
        await context.send("Invalid scope.")


#
async def setup(bot):
    await bot.add_cog(Sync(bot))
