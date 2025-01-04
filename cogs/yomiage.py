from api import GoogleTTS
import asyncio
import base64
import hashlib
import os
from logging import Logger
from database import D1
import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context # type: ignore

#
class Yomiage(commands.Cog, name="yomiage"):

    #
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.GoogleTTS = GoogleTTS()
        self.database = D1()
        self.logger = Logger("yomiage cog")

    #
    @commands.Cog.listener("on_message")
    async def yomiage(self, context: discord.Message) -> None:

        # Check if the message was sent by a bot
        if context.author.bot:
            return

        # Check if the message was sent by self
        if self.bot.user is not None and context.author.id == self.bot.user.id:
            return

        # Check if the message is empty
        if not context.content:
            return

        # Check if the message was sent in a guild
        if not context.guild:
            return

        # Check if the message includes a URL
        if "http" in context.content:
            return

        # Check if the bot is already connected to a voice channel
        if not context.guild.voice_client:
            return

        # Check if the message was sent in the target channel
        target_channel_id = await self.get_target_channel_id(context.guild.id)
        if target_channel_id != 0:
            if target_channel_id != context.channel.id:
                return
            if target_channel_id == None:
                return

        # Synthesize the audio
        file_path = await self.synthesize(context.content, context.author.id)
        if not file_path:
            return

        # Wait for the audio to finish playing
        voice_client = context.guild.voice_client
        if isinstance(voice_client, discord.VoiceClient):
            while voice_client.is_playing():
                await asyncio.sleep(1)
        else:
            return

        # Play the audio
        voice_client = context.guild.voice_client
        if isinstance(voice_client, discord.VoiceClient):
            voice_client.play(discord.FFmpegPCMAudio(file_path, before_options="-channel_layout mono"))

    #
    async def synthesize(self, text: str, user_id: int) -> str | None:

        #
        if self.bot.user is None:
            self.logger.error("Bot user is None")
            return None

        user = await self.get_user(user_id)
        if user is None:
            self.logger.error(f"Failed to get user settings for user_id {user_id}")
            return None

        #
        language: str = str(user["language"])
        voice: str = str(user["voice"])
        speakingrate: str = str(user["speakingrate"])
        pitch: str = str(user["pitch"])
        if not language or not voice or not speakingrate or not pitch:
            self.logger.error("Missing user settings")
            return None

        # Check if the cache exists
        hash_text: str = f"{text}{language}{voice}{speakingrate}{pitch}"
        hash: str = hashlib.md5(hash_text.encode()).hexdigest()
        file_path: str = f"cache/{hash}.wav"
        if not os.path.exists(file_path):

            # Synthesize the audio
            response: str = await self.GoogleTTS.synthesize(text, language, voice, speakingrate, pitch)
            if not response:
                self.logger.error("Failed to synthesize audio")
                return None

            # Save the audio
            with open(file_path, "wb") as file:
                file.write(base64.b64decode(response))

        #
        return file_path

    #
    async def get_target_channel_id(self, guild_id: int) -> int | None:

        # Get the target channel id
        result = self.database.get_target_channel_id(str(guild_id))
        if result is None:
            self.logger.error(f"Failed to get target channel id for guild_id {guild_id}")
            return None

        #
        return int(result)

    #
    async def get_user(self, user_id: int) -> dict[str, str] | None:
        return self.database.get_user_settings(str(user_id))

#
async def setup(bot: Bot) -> None:
    await bot.add_cog(Yomiage(bot))
