import asyncio
import base64
import hashlib
import requests

import discord
from discord.ext import commands
from discord.ext.commands import Context

#
class Yomiage(commands.Cog, name="yomiage"):

    #
    def __init__(self, bot):
        self.bot = bot

    #
    @commands.Cog.listener("on_message")
    async def yomiage(self, context: Context) -> None:

        # Check if the message was sent by a bot
        if context.author.bot:
            return

        # Check if the message was sent by self
        if context.author.id == self.bot.user.id:
            return

        # Check if the bot is already connected to a voice channel
        if context.guild.voice_client is None:
            return

        # Check if the message is empty
        if not context.content:
            return

        # Check if the message was sent in the target channel
        target_channel_id = await self.get_target_channel_id(context.guild.id)
        if context.channel.id != target_channel_id and target_channel_id != 0:
            return

        # Synthesize the audio
        file_path = await self.synthesize(context.content)

        # Wait for the audio to finish playing
        while context.guild.voice_client.is_playing():
            await asyncio.sleep(1)

        # Play the audio
        context.guild.voice_client.play(discord.FFmpegPCMAudio(file_path))

    #
    async def synthesize(self, text: str) -> str:

        #
        API_ENDPOINT = "https://texttospeech.googleapis.com/v1beta1/text:synthesize"

        #
        settings = await self.get_user(self.bot.user.id)
        if settings is None:
            self.bot.logger.error(f"Failed to get settings for user_id {self.bot.user.id}")
            return

        #
        headers = {
          'X-Goog-Api-Key': self.bot.config.get("google_api_key"),
          'Content-Type': 'application/json; charset=utf-8'
        }
        data = {
          'input': {
            'text': text
          },
          'voice': {
            'languageCode': settings["voice_languagecode"],
            'name': settings["voice_name"],
          },
          'audioConfig': {
            'audioEncoding': 'LINEAR16',
            'speakingRate': settings["audioconfig_speakingrate"],
            'pitch': settings["audioconfig_pitch"],
          }
        }

        # Request the audio
        response = requests.post(API_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        audio_data = response.json()["audioContent"]

        # Save the audio to a file
        hash = hashlib.md5(audio_data.encode()).hexdigest()
        file_path = f"cache/{hash}.wav"
        with open(file_path, "wb") as file:
            file.write(base64.b64decode(audio_data))

        #
        return file_path

    #
    async def get_target_channel_id(self, guild_id: int) -> int:
        result = self.bot.database.get_guild_by_guild_id(guild_id)
        return result["target_channel_id"]

    #
    async def get_user(self, user_id: int) -> dict:
        return self.bot.database.get_user_by_user_id(user_id)

#
async def setup(bot) -> None:
    await bot.add_cog(Yomiage(bot))
