import assemblyai as aai
import base64

aai.settings.api_key='26dedeac982341a19c376a123eeeeab3'

class AssemblyAISTT:

    def __init__(self, callback=None):
        self.sample_rate = 16000
        self.session_id = None
        self.transcriber = None
        self.callback = callback

    def start_session(self):
        self.transcriber = aai.RealtimeTranscriber(
            on_data=self.on_data,
            on_error=self.on_error,
            sample_rate=self.sample_rate,
            on_open=self.on_open,
            on_close=self.on_close
        )
        self.transcriber.connect()

    def send_audio(self, audio_data):
        self.transcriber.stream(audio_data)
    def get_microphone(self):
        microphone_stream = aai.extras.MicrophoneStream()
        self.transcriber.stream(microphone_stream)
    def end_session(self):
        self.transcriber.close()

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        self.session_id = session_opened.session_id
        print("Session ID:", self.session_id)

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            print(transcript.text, end="\r\n")
            if self.callback:
                self.callback(transcript.text)
        else:
            print(transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        print("An error occured:", error)

    def on_close(self):
        print("Closing Session")

# Utilisation
test = AssemblyAISTT(callback=lambda x: print(x))
test.start_session()
test.get_microphone()