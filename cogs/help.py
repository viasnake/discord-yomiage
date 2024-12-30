import discord
from discord.ext import commands
from discord.ext.commands import Context


#
class Help(commands.Cog, name="help"):

    #
    def __init__(self, bot):
        self.bot = bot

    #
    @commands.hybrid_command(
        name="help",
        description="Show available commands.",
    )
    async def help(self, context: Context) -> None:

        #
        embed = discord.Embed(
            title="Help",
            description="Available commands:",
            color=0x9C84EF,
        )

        # Add a field for each command
        for command in self.bot.commands:
            embed.add_field(
                name=f"/{command.name}",
                value=command.description,
                inline=False,
            )

        # Send the embed
        await context.send(embed=embed)


#
async def setup(bot) -> None:
    await bot.add_cog(Help(bot))
