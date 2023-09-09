import requests
import json
import os
import subprocess

class Lovo:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = 'https://api.lovo.ai/v1/conversion'
        self.headers = {
            'apiKey': '2bda943d-528f-49e3-aec3-f6826a0392f1',
            'Content-Type': 'application/json; charset=utf-8'
        }
    
    def generate_tts(self, text, speaker_id, emphasis, speed, pause):
        data = json.dumps({
            "text": text,
            "speaker_id": speaker_id,
            "emphasis": emphasis,
            "speed": speed,
            "pause": pause
        })
        res = requests.post(self.url, headers=self.headers, data=data)
        outfile='test.wav'
        with open(outfile, 'wb') as f:
            f.write(res.content)
        print(f'Audio content written to file "{outfile}"')    

    def play_audio(self, audio_file):
        if os.path.exists(audio_file):
            subprocess.call(['aplay', audio_file])
        else:
            print(f'File "{audio_file}" does not exist')

test1=Lovo('2bda943d-528f-49e3-aec3-f6826a0392f1')
test1.generate_tts('hello world','','','','')


