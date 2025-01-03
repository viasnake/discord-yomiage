import os
import sys
from cloudflare import Cloudflare
from config import ConfigLoader
from logger import Logger

#
class DatabaseManager:

    #
    def __init__(self, client: Cloudflare) -> None:

        #
        config = ConfigLoader()

        #
        self.client = client
        self.database_id = config.get("cloudflare_database_id")
        self.account_id = config.get("cloudflare_account_id")
        self.logger = Logger("DatabaseManager")

        #
        self.init_database()

    #
    def init_database(self) -> None:

        #
        if not os.path.isfile(f"{os.path.realpath(os.path.dirname(__file__))}/schema.sql"):
            sys.exit("schema.sql not found.")

        #
        with open(f"{os.path.realpath(os.path.dirname(__file__))}/schema.sql", "r") as file:
            schema = file.read()

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
    def get_guild_by_guild_id(self, guild_id: str) -> dict | None:

        #
        try:
            result = self.client.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql="SELECT * FROM guilds WHERE guild_id = ?",
                params=[str(guild_id)],
            )
            result_query = result[0].results
        except Exception as e:
            self.logger.error(f"Failed to get guild: {e}")
            return

        #
        if len(result_query) == 0:
            self.logger.error(f"No rows found for guild_id {guild_id}")
            self.add_guild(guild_id)
            return self.get_guild_by_guild_id(guild_id)

        #
        if len(result_query) > 1:
            self.logger.error(f"Multiple rows found for guild_id {guild_id}")
            self.delete_guild(guild_id)
            self.add_guild(guild_id)
            return self.get_guild_by_guild_id(guild_id)

        #
        return result_query[0]

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
    def get_user_by_user_id(self, user_id: str) -> dict | None:

        #
        try:
            result = self.client.d1.database.query(
                database_id=self.database_id,
                account_id=self.account_id,
                sql="SELECT * FROM users WHERE user_id = ?",
                params=[str(user_id)],
            )
            result_query = result[0].results
        except Exception as e:
            self.logger.error(f"Failed to get user: {e}")
            return

        #
        if len(result_query) == 0:
            self.logger.error(f"No rows found for user_id {user_id}")
            self.add_user(user_id)
            return self.get_user_by_user_id(user_id)

        #
        if len(result_query) > 1:
            self.logger.error(f"Multiple rows found for user_id {user_id}")
            self.delete_user(user_id)
            self.add_user(user_id)
            return self.get_user_by_user_id(user_id)

        #
        return result_query[0]

    def update_pitch(self, user_id: str, pitch: float) -> None:

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
                result = self.client.d1.database.query(
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
