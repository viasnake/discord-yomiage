import re
from api import GoogleTTS
from database import D1
from discord.ext import commands
from discord.ext.commands import Bot, Context # type: ignore
from logger import Logger

#
class Setting(commands.Cog, name="setting"):

    #
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.database = D1()
        self.logger = Logger("setting cog")

    #
    @commands.hybrid_command(
        name="setpitch",
        description="音声のピッチを設定する。",
    )
    async def set_pitch(self, context: Context, pitch: str) -> None:

        # Check if the pitch is within the valid range
        if not pitch.isdigit() or int(pitch) < -20 or int(pitch) > 20:
            await context.send("ピッチは -20 から 20 の間で指定してください。")
            return

        # Update the user's audio configuration
        self.database.update_pitch(str(context.author.id), pitch)
        await context.send(f"ピッチを {pitch} に設定しました。")

    #
    @commands.hybrid_command(
        name="setspeakingrate",
        description="音声の速度を設定する。",
    )
    async def set_speaking_rate(self, context: Context, speed: str) -> None:

        # Check if the speed is within the valid range
        if not speed.replace(".", "", 1).isdigit() or float(speed) < 0.25 or float(speed) > 4.0:
            await context.send("速度は 0.25 から 4.0 の間で指定してください。")
            return

        # Update the user's audio configuration
        self.database.update_speakingrate(str(context.author.id), speed)
        await context.send(f"速度を {speed} に設定しました。")

    #
    @commands.hybrid_command(
        name="setlanguage",
        description="音声の言語を設定する。",
    )
    async def set_language(self, context: Context, language: str) -> None:

        # Check if the language is in BCP-47 format
        if not re.match(r"^[a-z]{2}-[A-Z]{2}$", language):
            await context.send("言語は BCP-47 形式で指定してください。")
            return

        # Check if the language is valid
        voices = await self.get_voice(language)
        if len(voices) == 0:
            await context.send("無効な言語です。")
            return

        # Update the user's audio configuration
        self.database.update_language(str(context.author.id), language)
        await context.send(f"言語を {language} に設定しました。")

    #
    @commands.hybrid_command(
        name="setvoice",
        description="音声の種類を設定する。",
    )
    async def set_voice(self, context: Context, voice: str) -> None:

        # Check if the voice is valid
        settings = self.database.get_user_settings(str(context.author.id))
        if settings is None:
            self.database.add_user(str(context.author.id))
            settings = self.database.get_user_settings(str(context.author.id))
            return
        voices = await self.get_voice(settings["language"])
        if voice not in [voice["name"] for voice in voices]:
            await context.send("無効な音声です。利用可能な音声: " + ", ".join([voice["name"] for voice in voices]))
            return

        # Update the user's audio configuration
        self.database.update_voice(str(context.author.id), voice)
        await context.send(f"音声を {voice} に設定しました.")

    #
    @commands.hybrid_command(
        name="setchannel",
        description="読み上げるチャンネルを設定する。",
    )
    async def set_target_channel(self, context: Context, scope: str = "global") -> None:

        # Check if the scope is valid
        if scope not in ["global", "local"]:
            await context.send("スコープは global または local で指定してください。")
            return

        # Set the target channel to global
        if scope == "global":
            self.database.update_target_channel(str(context.author.id), "0")
            await context.send("読み上げ対象のチャンネルを全チャンネルに設定しました。")
            return

        # Set the target channel to local
        self.database.update_target_channel(str(context.author.id), str(context.channel.id))
        await context.send(f"読み上げ対象のチャンネルをこのチャンネルに設定しました。")

    #
    async def get_voice(self, language: str) -> list[dict[str, str]]:
        return await GoogleTTS().voices(language)

#
async def setup(bot: Bot) -> None:
    await bot.add_cog(Setting(bot))
