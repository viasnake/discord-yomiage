import re
from api import GoogleTTS
from database import D1
import discord
from discord.ext import commands
from discord import SelectOption
from discord.ext.commands import Bot, Context # type: ignore
from logger import Logger


#
class Dropdown(discord.ui.Select):

        #
        def __init__(self, options: list[SelectOption], database: D1, custom_id: str, placeholder: str = "選択してください。") -> None:
            super().__init__(placeholder=placeholder, min_values=1, max_values=1, options=options, custom_id=custom_id)
            self.database = database

        #
        async def callback(self, interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            value = self.values[0]

            # Determine the update function based on the dropdown ID
            if self.custom_id == "voice":
                self.database.update_voice(str(interaction.user.id), value)
            elif self.custom_id == "language":
                self.database.update_language(str(interaction.user.id), value)

            await interaction.followup.send(f"{value} に設定しました。", ephemeral=True)

            #
            if interaction.message:
                await interaction.message.delete()

#
class DropdownView(discord.ui.View):

        #
        def __init__(self, dropdown: Dropdown) -> None:
            super().__init__()
            self.timeout = 60
            self.add_item(dropdown)

        #
        async def on_timeout(self) -> None:

            # Delete the dropdown
            self.stop()

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
        if int(pitch) < -20 or int(pitch) > 20:
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
    async def set_language(self, context: Context) -> None:

        # Defer the response
        await context.defer()

        # Get the available languages
        languages = await self.get_available_languages()

        # Create the dropdown
        options = [SelectOption(label=f"{language['code']}", description=language['name'], emoji=language['flag']) for language in languages.values()]
        dropdown = Dropdown(options, self.database, "language", "言語を選択してください。")
        view = DropdownView(dropdown)

        # Send the message
        await context.send("言語を選択してください。", view=view)

    #
    @commands.hybrid_command(
        name="setvoice",
        description="音声の種類を設定する。",
    )
    async def set_voice(self, context: Context) -> None:

        # Defer the response
        await context.defer()

        # Get the user's settings
        settings = self.database.get_user_settings(str(context.author.id))
        if settings is None:
            self.database.add_user(str(context.author.id))
            settings = self.database.get_user_settings(str(context.author.id))
            return

        # Get the available voices
        voices = await self.get_voice(settings["language"])
        if len(voices) == 0:
            await context.send("音声が見つかりませんでした。")
            return

        # Create the dropdown
        options = [SelectOption(label=voice["name"], description=voice["name"]) for voice in voices]
        dropdown = Dropdown(options, self.database, "voice", "音声を選択してください。")
        view = DropdownView(dropdown)

        # Send the message
        await context.send("音声を選択してください。", view=view)

    #
    @commands.hybrid_command(
        name="setchannel",
        description="読み上げるチャンネルを設定する。",
    )
    async def set_target_channel(self, context: Context, scope: str = "local") -> None:

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
    async def get_voice(self, language: str = "") -> list[dict[str, str]]:
        return await GoogleTTS().voices(language)

    #
    async def get_available_languages(self) -> dict[str, dict[str, str]]:
        languages = {
            "en-US": {
                "name": "English (United States)",
                "code": "en-US",
                "flag": "🇺🇸",
            },
            "en-GB": {
                "name": "English (United Kingdom)",
                "code": "en-GB",
                "flag": "🇬🇧",
            },
            "en-AU": {
                "name": "English (Australia)",
                "code": "en-AU",
                "flag": "🇦🇺",
            },
            "en-IN": {
                "name": "English (India)",
                "code": "en-IN",
                "flag": "🇮🇳",
            },
            "ja-JP": {
                "name": "日本語",
                "code": "ja-JP",
                "flag": "🇯🇵",
            },
            "cmn-CN": {
                "name": "普通话",
                "code": "cmn-CN",
                "flag": "🇨🇳",
            },
            "yue-HK": {
                "name": "粤語",
                "code": "yue-HK",
                "flag": "🇭🇰",
            },
            "ko-KR": {
                "name": "한국어",
                "code": "ko-KR",
                "flag": "🇰🇷",
            },
            "de-DE": {
                "name": "Deutsch",
                "code": "de-DE",
                "flag": "🇩🇪",
            },
            "fr-FR": {
                "name": "Français",
                "code": "fr-FR",
                "flag": "🇫🇷",
            },
            "es-ES": {
                "name": "Español",
                "code": "es-ES",
                "flag": "🇪🇸",
            },
            "it-IT": {
                "name": "Italiano",
                "code": "it-IT",
                "flag": "🇮🇹",
            },
        }

        return languages


#
async def setup(bot: Bot) -> None:
    await bot.add_cog(Setting(bot))
