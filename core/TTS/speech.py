from typing import Optional
from elevenlabs import generate, play, set_api_key
from TTS.default import low_level_stt
class Speech:
    def __init__(self, text: str, provider: Optional[str] = "elevenlabs"):
        self.text = text
        self.provider = provider
        self.api_key = ""

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
        elif self.provider=="local":
             r=low_level_stt().text_to_speech(self.text,'en')
        else:
            raise NotImplementedError("Provider not implemented yet")

    def play_audio(self):
        if self.provider == "local":
            print(self.text)
            return self.generate_audio()
        elif self.provider=="elevenlabs":
             audio = self.generate_audio()
             play(audio)
        else:
            print('no others')

#test
