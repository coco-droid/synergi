import json
import re
from llms.llms import Model
#from memory.episodic import EpisodicMemory
from agent.contextual import ContextConversation

PROMPT_PREDICT_KEYS = """
En vous basant sur le contexte conversationnel fourni, prédire une liste de 1 à 5 clés candidates dans la mémoire épisodique pouvant être pertinentes:
"""

class IntentAnalyzer:

  def __init__(self):

    #self.episodic_memory = EpisodicMemory('synergi_index') 
    self.context = ContextConversation()

    self.master_prompt = '''You are Synergi, an AI assistant created to be helpful, harmless, and honest. Your objective is to analyze conversations with users and take appropriate actions to assist them.

When a user sends a message, you should parse their request, then return a simple JSON object containing relevant fields:

intent - The inferred intent or goal behind the user's message.
output - The text response you should display to the user.
action - Any actions you should execute, like launching a task.
goal - The user's overall goal if explicitly stated.
steps - Step-by-step instructions to achieve the goal.
predicted_keys - Any potentially relevant memories you should retrieve to assist the user
EXAMPLE OF JSON OBJECT TO RETURN:
{
  "intent": "",
  "output": "",
  "action": "",
  "goal": "",
  "steps":[],
  "predicted_keys": []
}

'''

    self.model = Model("jurassic", master_prompt=self.master_prompt, api_key="VOTRE_CLEF")
    self.key_predictor = Model("jurassic", prompt=PROMPT_PREDICT_KEYS, api_key="VOTRE_CLEF")

  def predict(self, message):

    #context = self.context.get_recent_context()
    context ="a simple conversation"
    # Prédire clés candidates
    #predicted_keys = self.key_predictor.generate_text(context)  

    # Analyser intention 
    context_str = "the context: " + context
    user_message_str = "the user message: " + message

    full_prompt = context_str + "\n" + user_message_str

    def extract_json(text):

      # Trouver le JSON valide dans le texte
      match = re.search(r'({.+})', text)
      if match:
        json_str = match.group(1)

        try:
          data = json.loads(json_str)
          return data
        except JSONDecodeError:
          print("JSON invalide")

      # Sinon, tenter de parser directement tout le texte    
      try:
        data = json.loads(text)
        return data
      except JSONDecodeError:
        print("Pas de JSON valide trouvé")

      return None

    response = self.model.generate_text(full_prompt)
    data = extract_json(response)

    # Mettre à jour clés prédites
    #data["predicted_keys"] = predicted_keys

    if "memorize" in data:
      for element in data["memorize"]:
        key = generate_key()  
        #self.episodic_memory.save(element, key) 

    #function to delete all null key in data
    data = {k: v for k, v in data.items() if v is not None}
    print(f"IntentAnalyzer: {data}")
    return data
