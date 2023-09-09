import pyaudio
from assembly import AssemblyAISTT
from typing import Callable
from threading import Thread
import time

class STT:
    def __init__(self,provider):
        self.user_voice = None
        self.transcript = None
        self.provider = None
        if provider == "assembly":
            self.provider = AssemblyAISTT()
        else:
            raise Exception("Provider not supported")

    def start_session(self):
         self.user_voice=self.generate_stream()
         self.provider.start_session()
         self.transcript = stt.send_audio(self.user_voice)
         print(self.transcript)
         # detect when we have new transcript
    def end_session(self):
        self.provider.end_session()
        self.user_voice = None
        self.transcript = None
    def generate_stream(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        return stream



test = STT("assembly")
test.start_session()