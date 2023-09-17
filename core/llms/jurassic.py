import requests
import json
from params.config import APIKeyManager
class Jurassic:

  def __init__(self, api_key):
    self.api_key =APIKeyManager().get_api_key('jurassic_key')
    self.base_url = "https://api.ai21.com/studio/v1/"

  def generate(self, prompt, model="j2-ultra"):
    print(f"Prompt: {prompt}")
    url = f"{self.base_url}{model}/complete"

    headers = {
      "Authorization": f"Bearer {self.api_key}",
      "Content-Type": "application/json" 
    }

    data = {
      "prompt": prompt,
      "numResults": 1,
      "maxTokens": 100, 
      "stopSequences": ["."],
      "topKReturn": 0, 
      "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    result = json.loads(response.text)
    text = result['completions'][0]['data']['text']
    print(f"Text: {text}")
    return text