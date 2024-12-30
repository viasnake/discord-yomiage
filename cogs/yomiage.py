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
        # Check if the message is valid
        ALLOWED_CHANNEL_NAMES = ["yomiage"]
        if not any(
            context.channel.name.startswith(channel_name)
            for channel_name in ALLOWED_CHANNEL_NAMES
        ):
            return
        if context.guild.voice_client is None:
            return
        if len(context.content) > 100:
            return
        if any(
            word in context.content
            for word in ["http", "www.", ".com", ".net", ".org", ".jp", "@"]
        ):
            return

        # Replace special characters
        context.content = context.content.replace("\n", "")
        context.content = context.content.replace("\r", "")
        context.content = context.content.replace("\t", "")

        # Generate the audio
        generated_audio = await self.synthesize(context.content)

        # Wait until the bot finishes playing the current audio
        while context.guild.voice_client.is_playing():
            await asyncio.sleep(1)

        # Play the audio
        context.guild.voice_client.play(discord.FFmpegPCMAudio(generated_audio))

    #
    async def synthesize(self, text: str) -> str:
        API_ENDPOINT = "https://texttospeech.googleapis.com/v1beta1/text:synthesize"

        headers = {
          'X-Goog-Api-Key': self.bot.config["API_KEY"],
          'Content-Type': 'application/json; charset=utf-8'
        }

        data = {
          'input': {
            'text': text
          },
          'voice': {
            'languageCode': 'ja-JP',
            'name': 'ja-JP-Wavenet-C',
          },
          'audioConfig': {
            'audioEncoding': 'LINEAR16',
            'speakingRate': 1.4,
          }
        }

        # cache the audio
        md5_hash = hashlib.md5(text.encode()).hexdigest()
        file_path = f"cache/{md5_hash}.wav"
        try:
            with open(file_path, "rb") as file:
                return file_path
        except FileNotFoundError:
            response = requests.post(API_ENDPOINT, headers=headers, json=data)
            response.raise_for_status()

            # Decode the audio data
            audio_data = response.json()["audioContent"]
            audio_bytes = base64.b64decode(audio_data)

            # Save the audio to a file
            with open(file_path, "wb") as file:
                file.write(audio_bytes)

        return file_path


    #
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.guild.voice_client is None:
            return
        if before.channel is None:
            return
        if before.channel != after.channel:
            if len(before.channel.members) == 1:
                await before.channel.guild.voice_client.disconnect()

    #
    @commands.hybrid_command(
        name="connect",
        description="Connect to the voice channel",
    )
    async def connect(self, context: Context):
        if context.author.voice is None:
            await context.send("You are not connected to a voice channel.")
            return

        if context.guild.voice_client is not None:
            await context.send("I am already connected to a voice channel.")
            return

        await context.author.voice.channel.connect()
        await context.send(f"Connected to {context.author.voice.channel.name}")

    #
    @commands.hybrid_command(
        name="disconnect",
        description="Disconnect from the voice channel",
    )
    async def disconnect(self, context: Context):
        if context.guild.voice_client is None:
            await context.send("I am not connected to a voice channel.")
            return

        await context.guild.voice_client.disconnect()
        await context.send("Disconnected.")

    # auto disconnect
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
    await bot.add_cog(Yomiage(bot))
