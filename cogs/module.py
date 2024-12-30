from discord.ext import commands
from discord.ext.commands import Context


#
class Module(commands.Cog, name="module"):

    #
    def __init__(self, bot):
        self.bot = bot

    #
    @commands.hybrid_command(
        name="load",
        description="Load a module.",
    )
    @commands.is_owner()
    async def load(self, context: Context, module: str) -> None:

        #
        await context.send(f"Trying to load the `{module}` module...")

        #
        try:
            await self.bot.load_extension(f"cogs.{module}")
        except Exception:
            await context.send(f"Failed to load the `{module}` module.")
            return

        #
        await context.send(f"Successfully loaded the `{module}` module.")

    #
    @commands.hybrid_command(
        name="unload",
        description="Unload a module.",
    )
    @commands.is_owner()
    async def unload(self, context: Context, module: str) -> None:

        #
        await context.send(f"Trying to unload the `{module}` module...")

        #
        try:
            await self.bot.unload_extension(f"cogs.{module}")
        except Exception:
            await context.send(f"Failed to unload the `{module}` module.")
            return

        #
        await context.send(f"Successfully unloaded the `{module}` module.")

    #
    @commands.hybrid_command(
        name="reload",
        description="Reload a module.",
    )
    @commands.is_owner()
    async def reload(self, context: Context, module: str) -> None:

        #
        await context.send(f"Trying to reload the `{module}` module...")

        #
        try:
            await self.bot.reload_extension(f"cogs.{module}")
        except Exception:
            await context.send(f"Failed to reload the `{module}` module.")
            return

        #
        await context.send(f"Successfully reloaded the `{module}` module.")

#
async def setup(bot):
    await bot.add_cog(Module(bot))
