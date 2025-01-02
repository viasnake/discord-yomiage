import re
from discord.ext import commands
from discord.ext.commands import Context

#
class Setting(commands.Cog, name="setting"):

    #
    def __init__(self, bot):
        self.bot = bot

    #
    @commands.hybrid_command(
        name="setpitch",
        description="音声のピッチを設定する。",
    )
    async def set_pitch(self, context: Context, pitch: float) -> None:

        # Check if the pitch is within the valid range
        if pitch < -20 or pitch > 20:
            await context.send("ピッチは -20 から 20 の間で指定してください。")
            return

        # Update the user's audio configuration
        await self.bot.database.update_user_audioconfig_pitch(context.author.id, pitch)
        await context.send(f"ピッチを {pitch} に設定しました。")

    #
    @commands.hybrid_command(
        name="setspeakingrate",
        description="音声の速度を設定する。",
    )
    async def set_speaking_rate(self, context: Context, speed: float) -> None:

        # Check if the speed is within the valid range
        if speed < 0.25 or speed > 4.0:
            await context.send("速度は 0.25 から 4.0 の間で指定してください。")
            return

        # Update the user's audio configuration
        await self.bot.database.update_user_audioconfig_speakingrate(context.author.id, speed)
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

        # Update the user's audio configuration
        await self.bot.database.update_user_audioconfig_languagecode(context.author.id, language)
        await context.send(f"言語を {language} に設定しました。")

    #
    @commands.hybrid_command(
        name="setvoice",
        description="音声の種類を設定する。",
    )
    async def set_voice(self, context: Context, voice: str) -> None:

        # FIXME: NEEDS MORE ITELIGENCE HERE
        if voice not in ["ja-JP-Wavenet-A", "ja-JP-Wavenet-B", "ja-JP-Wavenet-C", "ja-JP-Wavenet-D"]:
            await context.send("音声は ja-JP-Wavenet-A, ja-JP-Wavenet-B, ja-JP-Wavenet-C, ja-JP-Wavenet-D のいずれかを指定してください。")
            return

        # Update the user's audio configuration
        await self.bot.database.update_user_audioconfig_voice(context.author.id, voice)
        await context.send(f"音声を {voice} に設定しました.")

#
async def setup(bot) -> None:
    await bot.add_cog(Setting(bot))
