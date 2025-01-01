from discord.ext import commands
from discord.ext.commands import Context

#
class Voice(commands.Cog, name="voice"):

    #
    def __init__(self, bot):
        self.bot = bot

    #
    @commands.hybrid_command(
        name="connect",
        description="ボイスチャンネルに接続する。",
    )
    async def connect(self, context: Context):

        # Check if the author is in a voice channel
        if context.author.voice is None:
            self.bot.logger.info(f"{context.author} is not in a voice channel.")
            await context.send("ボイスチャンネルに接続してください。")
            return

        # Check if the bot is already connected to a voice channel
        if context.guild.voice_client is not None:
            self.bot.logger.info(f"{context.guild.voice_client} is already connected to a voice channel.")
            await context.send("すでにボイスチャンネルに接続しています。")
            return

        # Connect to the voice channel
        await context.author.voice.channel.connect()
        self.bot.logger.info(f"Connected to {context.author.voice.channel.name}.")
        await context.send(f"{context.author.voice.channel.name} に接続しました。")

    #
    @commands.hybrid_command(
        name="disconnect",
        description="ボイスチャンネルから切断する。",
    )
    async def disconnect(self, context: Context):

        # Check if the bot is connected to a voice channel
        if context.guild.voice_client is None:
            self.bot.logger.info(f"{context.guild.voice_client} is not connected to a voice channel.")
            await context.send("ボイスチャンネルに接続していません。")
            return

        # Disconnect from the voice channel
        await context.guild.voice_client.disconnect()
        self.bot.logger.info(f"Disconnected from {context.author.voice.channel.name}.")
        await context.send(f"ボイスチャンネルから切断しました。")

    #
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        # Check if the bot is connected to a voice channel
        if member.guild.voice_client is None:
            return

        # Check if the member is the only one in the channel
        if before.channel is None:
            return

        # Check if the member moved to a different channel
        if before.channel != after.channel:

            # Disconnect if the bot is the only one in the channel
            if len(before.channel.members) == 1:
                await before.channel.guild.voice_client.disconnect()

            # Disconnect if all members is bot
            if all(member.bot for member in before.channel.members):
                await before.channel.guild.voice_client.disconnect()

#
async def setup(bot) -> None:
    await bot.add_cog(Voice(bot))
