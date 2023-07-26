from typing import Optional
from elevenlabs import generate, play, set_api_key

class Speech:
    def __init__(self, text: str, provider: Optional[str] = "elevenlabs"):
        self.text = text
        self.provider = provider
        self.api_key = None

    def set_api_key(self, api_key: str):
        self.api_key = api_key

    def generate_audio(self):
        if self.provider == "elevenlabs":
            set_api_key(self.api_key)
            audio = generate(
                text=self.text,
                voice="Bella",
                model='eleven_monolingual_v1'
            )
            return audio
        else:
            raise NotImplementedError("Provider not implemented yet")

    def play_audio(self):
        audio = self.generate_audio()
        play(audio)
