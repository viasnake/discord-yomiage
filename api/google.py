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
        self.V1_API_ENDPOINT: str = "https://texttospeech.googleapis.com/v1"

        #
        self.api_key: str = config.get("google_api_key")
        self.logger = Logger("GoogleTTS")

    #
    async def voices(self, language_code: str) -> list[dict[str, str]]:

        #
        QUERY: str = f"?languageCode={language_code}"
        API_ENDPOINT: str = f"{self.V1_API_ENDPOINT}/voices{QUERY}"

        #
        headers: dict[str, str] = {
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
        return response.json().get("voices", [])

    #
    async def synthesize(self, text: str, language: str, voice: str, speakingrate: str, pitch: str) -> str:

        #
        API_ENDPOINT: str = f"{self.V1_API_ENDPOINT}/text:synthesize"

        #
        headers: dict[str, str] = {
          'X-Goog-Api-Key': self.api_key,
          'Content-Type': 'application/json; charset=utf-8'
        }
        body: dict[str, dict[str, str]] = {
          'input': {
            'text': text,
          },
          'voice': {
            'languageCode': language,
            'name': voice
          },
          'audioConfig': {
            'audioEncoding': 'LINEAR16',
            'speakingRate': speakingrate,
            'pitch': pitch
          }
        }

        #
        response: requests.Response = requests.post(API_ENDPOINT, headers=headers, json=body)
        response.raise_for_status()

        #
        if response.status_code != 200:
            raise Exception(f"Failed to synthesize text: {response.text}")

        #
        return response.json()["audioContent"]
