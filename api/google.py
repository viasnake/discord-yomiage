import requests
from config import ConfigLoader
from logger import Logger

#
class GoogleTTS:

    #
    def __init__(self) -> None:

        #
        config = ConfigLoader()

        #
        self.V1_API_ENDPOINT = "https://texttospeech.googleapis.com/v1"

        #
        self.api_key = config.get("google_api_key")
        self.logger = Logger("GoogleTTS")

    #
    def voices(self, language_code: str) -> dict:

        #
        QUERY = f"?languageCode={language_code}"
        API_ENDPOINT = f"{self.V1_API_ENDPOINT}/voices{QUERY}"

        #
        headers = {
          'X-Goog-Api-Key': self.api_key,
          'Content-Type': 'application/json; charset=utf-8'
        }

        #
        response = requests.get(API_ENDPOINT, headers=headers)
        response.raise_for_status()

        #
        if response.status_code != 200:
            raise Exception(f"Failed to get voices: {response.text}")

        #
        return response.json()

    #
    def synthesize(self, text: str, voice_language_code: str, voice_name: str, audioconfig_speakingrate: float, audioconfig_pitch: float) -> str:

        #
        API_ENDPOINT = f"{self.V1_API_ENDPOINT}/text:synthesize"

        #
        headers = {
          'X-Goog-Api-Key': self.api_key,
          'Content-Type': 'application/json; charset=utf-8'
        }
        body = {
          'input': {
            'text': text
          },
          'voice': {
            'languageCode': voice_language_code,
            'name': voice_name,
          },
          'audioConfig': {
            'audioEncoding': 'LINEAR16',
            'speakingRate': audioconfig_speakingrate,
            'pitch': audioconfig_pitch,
          }
        }

        #
        response = requests.post(API_ENDPOINT, headers=headers, json=body)
        response.raise_for_status()

        #
        if response.status_code != 200:
            raise Exception(f"Failed to synthesize text: {response.text}")

        #
        return response.json()["audioContent"]
