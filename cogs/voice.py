import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context # type: ignore
from logger import Logger

#
class Voice(commands.Cog, name="voice"):

    #
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.logger = Logger("voice cog")

    #
    @commands.hybrid_command(
        name="connect",
        description="ボイスチャンネルに接続する。",
    )
    async def connect(self, context: Context) -> None:

        # Check if the author is in a voice channel
        if not isinstance(context.author, discord.Member) or context.author.voice is None:
            await context.send("ボイスチャンネルに接続してください。")
            return

        # Check if the bot is already connected to a voice channel
        if discord.utils.get(context.bot.voice_clients, guild=context.guild) is not None:
            await context.send("すでにボイスチャンネルに接続しています。")
            return

        # Connect to the voice channel
        if context.author.voice and context.author.voice.channel:
            await context.author.voice.channel.connect()
        else:
            await context.send("ボイスチャンネルに接続できませんでした。")
            return

        # Send a message
        if context.author.voice and context.author.voice.channel:
            await context.send(f"{context.author.voice.channel.name} に接続しました。")
        else:
            await context.send("ボイスチャンネルに接続できませんでした。")
            return

    #
    @commands.hybrid_command(
        name="disconnect",
        description="ボイスチャンネルから切断する。",
    )
    async def disconnect(self, context: Context) -> None:

        # Check if the bot is connected to a voice channel
        if discord.utils.get(context.bot.voice_clients, guild=context.guild) is None:
            await context.send("ボイスチャンネルに接続していません。")
            return

        # Disconnect from the voice channel
        voice_client = discord.utils.get(context.bot.voice_clients, guild=context.guild)
        if voice_client is not None:
            await voice_client.disconnect(force=True)
        else:
            await context.send("ボイスチャンネルから切断できませんでした。")
            return

        # Send a message
        await context.send(f"ボイスチャンネルから切断しました。")

    #
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:

        # Check if the bot is connected to a voice channel
        if member.guild.voice_client is None:
            return

        # Check if the member is the only one in the channel
        if before.channel is None:
            return

        # Check if the member moved to a different channel
        if before.channel != after.channel:

            # Disconnect if the bot is the only one in the channel
            if before.channel.guild.voice_client is None:
                return

            # Disconnect if the bot is the only one in the channel
            if len(before.channel.members) == 1:
                await before.channel.guild.voice_client.disconnect(force=True)
                return

            # Disconnect if all members is bot
            if all(member.bot for member in before.channel.members):
                await before.channel.guild.voice_client.disconnect(force=True)
                return

#
async def setup(bot: Bot) -> None:
    await bot.add_cog(Voice(bot))
