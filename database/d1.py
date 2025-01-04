import os
import sys
from typing import List, Any
from cloudflare import Cloudflare
from cloudflare.types.d1 import QueryResult
from config import ConfigLoader
from logger import Logger

#
class D1:

    #
    def __init__(self) -> None:

        #
        config = ConfigLoader()

        #
        self.client = Cloudflare(
            api_token=config.get("cloudflare_api_token"),
        )
        self.database_id: str = config.get("cloudflare_database_id")
        self.account_id: str = config.get("cloudflare_account_id")

        #
        self.logger = Logger("CloudflareD1")

    #
    def init_database(self) -> None:

        #
        if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/schema.sql"):
            sys.exit("schema.sql not found.")

        #
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/schema.sql", "r") as file:
            schema: str = file.read()

        #
        try:
            self.client.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql=schema,
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize the database: {e}")

    #
    def add_guild(self, guild_id: str) -> None:

        #
        try:
            self.client.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql="INSERT INTO guilds (guild_id) VALUES (?)",
                params=[str(guild_id)],
            )
        except Exception as e:
            self.logger.error(f"Failed to add guild: {e}")
            return

        #
        self.logger.info(f"Added guild {guild_id}")

    #
    def delete_guild(self, guild_id: str) -> None:

        #
        try:
            self.client.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql="DELETE FROM guilds WHERE guild_id = ?",
                params=[str(guild_id)],
            )
        except Exception as e:
            self.logger.error(f"Failed to delete guild: {e}")
            return

        #
        self.logger.info(f"Deleted guild {guild_id}")

    #
    def get_target_channel_id(self, guild_id: str) -> str | None:

            #
            try:
                result: List[QueryResult] = self.client.d1.database.query(
                    database_id=self.database_id,
                    account_id=self.account_id,
                    sql="SELECT * FROM guilds WHERE guild_id = ?",
                    params=[str(guild_id)],
                )
            except Exception as e:
                self.logger.error(f"Failed to get target_channel_id: {e}")
                return

            #
            if not result:
                self.logger.error(f"Failed to get target_channel_id: {result}")
                return

            #
            if not result[0].results:
                self.logger.error(f"Failed to get target_channel_id: {result[0].results}")
                return

            #
            if len(result[0].results) == 0:
                self.logger.error(f"No rows found for guild_id {guild_id}")
                self.add_guild(guild_id)
                return self.get_target_channel_id(guild_id)

            #
            if len(result[0].results) > 1:
                self.logger.error(f"Multiple rows found for guild_id {guild_id}")
                self.delete_guild(guild_id)
                self.add_guild(guild_id)
                return self.get_target_channel_id(guild_id)

            return result[0].results[0]["target_channel_id"] # type: ignore

    #
    def add_user(self, user_id: str) -> None:

        #
        try:
            self.client.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql="INSERT INTO users (user_id) VALUES (?)",
                params=[str(user_id)],
            )
        except Exception as e:
            self.logger.error(f"Failed to add user: {e}")
            return

        #
        self.logger.info(f"Added user {user_id}")

    #
    def delete_user(self, user_id: str) -> None:

        #
        try:
            self.client.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql="DELETE FROM users WHERE user_id = ?",
                params=[str(user_id)],
            )
        except Exception as e:
            self.logger.error(f"Failed to delete user: {e}")
            return

        #
        self.logger.info(f"Deleted user {user_id}")

    #
    def get_user_settings(self, user_id: str) -> dict[str, str] | None:

        #
        try:
            result: List[QueryResult] = self.client.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql="SELECT * FROM users WHERE user_id = ?",
                params=[str(user_id)],
            )
        except Exception as e:
            self.logger.error(f"Failed to get user: {e}")
            return

        #
        if not result:
            self.logger.error(f"Failed to get user")
            return

        #
        if not result[0].results:
            self.logger.error(f"Failed to get user")
            return

        #
        if len(result[0].results) == 0:
            self.logger.error(f"No rows found for user_id {user_id}")
            self.add_user(user_id)
            return self.get_user_settings(user_id)

        #
        if len(result[0].results) > 1:
            self.logger.error(f"Multiple rows found for user_id {user_id}")
            self.delete_user(user_id)
            self.add_user(user_id)
            return self.get_user_settings(user_id)

        return {
            "language": result[0].results[0]["language"], # type: ignore
            "pitch": result[0].results[0]["pitch"], # type: ignore
            "speakingrate": result[0].results[0]["speakingrate"], # type: ignore
            "voice": result[0].results[0]["voice"], # type: ignore
        }

    def update_pitch(self, user_id: str, pitch: str) -> None:

        #
        try:
            self.client.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql="UPDATE users SET pitch = ? WHERE user_id = ?",
                params=[str(pitch), str(user_id)],
            )
        except Exception as e:
            self.logger.error(f"Failed to update pitch: {e}")
            return

        #
        self.logger.info(f"Updated pitch: user {user_id}")

    def update_speakingrate(self, user_id: str, speakingrate: str) -> None:

        #
        try:
            self.client.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql="UPDATE users SET speakingrate = ? WHERE user_id = ?",
                params=[str(speakingrate), str(user_id)],
            )
        except Exception as e:
            self.logger.error(f"Failed to update speakingrate: {e}")
            return

        #
        self.logger.info(f"Updated speakingrate: user {user_id}")

    def update_language(self, user_id: str, language: str) -> None:

        #
        try:
            self.client.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql="UPDATE users SET language = ? WHERE user_id = ?",
                params=[str(language), str(user_id)],
            )
        except Exception as e:
            self.logger.error(f"Failed to update language: {e}")
            return

        #
        self.logger.info(f"Updated language: user {user_id}")

    def update_voice(self, user_id: str, voice: str) -> None:

        #
        try:
            self.client.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql="UPDATE users SET voice = ? WHERE user_id = ?",
                params=[str(voice), str(user_id)],
            )
        except Exception as e:
            self.logger.error(f"Failed to update voice: {e}")
            return

        #
        self.logger.info(f"Updated voice: user {user_id}")

    def update_target_channel(self, guild_id: str, channel_id: str) -> None:

            #
            try:
                self.client.d1.database.query(
                    database_id=self.database_id,
                    account_id=self.account_id,
                    sql="UPDATE guilds SET target_channel_id = ? WHERE guild_id = ?",
                    params=[str(channel_id), str(guild_id)],
                )
            except Exception as e:
                self.logger.error(f"Failed to update target_channel_id: {e}")
                return

            #
            self.logger.info(f"Updated target_channel_id: guild {guild_id}, channel {channel_id}")
