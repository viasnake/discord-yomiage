import os
import sys
from cloudflare import Cloudflare
from config import ConfigLoader

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
        self.client.d1.database.query(
            database_id=self.database_id,
            account_id=self.account_id,
            sql=schema,
        )

    #
    def add_user(self, user_id: int) -> None:
        self.client.d1.database.query(
            database_id=self.database_id,
            account_id=self.account_id,
            sql=f"INSERT INTO users (user_id) VALUES (?)",
            params=[user_id],
        )

    #
    def get_user(self, user_id: int) -> dict:
        return self.client.d1.database.query(
            database_id=self.database_id,
            account_id=self.account_id,
            sql=f"SELECT * FROM users WHERE user_id = ?",
            params=[user_id],
        )

    #
    def update_user_voice_languagecode(self, user_id: int, languagecode: str) -> None:
        self.client.d1.database.query(
            database_id=self.database_id,
            account_id=self.account_id,
            sql=f"UPDATE users SET voice_languagecode = ? WHERE user_id = ?",
            params=[languagecode, user_id],
        )

    #
    def update_user_voice_name(self, user_id: int, name: str) -> None:
        self.client.d1.database.query(
            database_id=self.database_id,
            account_id=self.account_id,
            sql=f"UPDATE users SET voice_name = ? WHERE user_id = ?",
            params=[name, user_id],
        )

    #
    def update_user_audioconfig_speakingrate(self, user_id: int, speakingrate: int) -> None:
        self.client.d1.database.query(
            database_id=self.database_id,
            account_id=self.account_id,
            sql=f"UPDATE users SET audioconfig_speakingrate = ? WHERE user_id = ?",
            params=[speakingrate, user_id],
        )

    #
    def update_user_audioconfig_pitch(self, user_id: int, pitch: int) -> None:
        self.client.d1.database.query(
            database_id=self.database_id,
            account_id=self.account_id,
            sql=f"UPDATE users SET audioconfig_pitch = ? WHERE user_id = ?",
            params=[pitch, user_id],
        )
