import speech_recognition as sr
import openai

class SpeechToText:
    def __init__(self, api_key):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        openai.api_key = api_key

    def recognize_audio(self,name):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while True:
                audio = self.recognizer.listen(source)
                try:
                    print("Recognizing...")
                    text = self.recognizer.recognize_whisper_api(audio)
                    if name in text.lower():
                       command = text.lower().split(name)[1]
                       print (f"User said: {command}");
                       return command
                    else:
                        print("Could not understand audio")
                        print(text)
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:                    print(f"Could not request results from Google Speech Recognition service; {e}")

test=SpeechToText("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")
test.recognize_audio('claude')

