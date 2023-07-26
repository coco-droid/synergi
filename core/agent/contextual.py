import json
from datetime import datetime
from llms.llms import Model

SUMMARIZE_PROMPT = "Générez un résumé concis de la conversation ci-dessous :"

class ContextConversation:

  MAX_HISTORY = 5
  
  def __init__(self):
    self.recent_history = []
    self.long_history = [] 
    self.conversation_goals = []
    self.current_summary = None

  def update(self, message, response):

    # Mise à jour des historiques
    self.recent_history.append((message, response))  
    if len(self.recent_history) > self.MAX_HISTORY:
        self.recent_history = self.recent_history[-self.MAX_HISTORY:]
    self.long_history.append((message, response))

    # Génération du résumé avec GPT-4
    history = self.long_history
    context = ""
    for msg, resp in history:
      context += f"Utilisateur: {msg}\nSynergi: {resp}\n"
    
    summarizer = Model("jurassic", SUMMARIZE_PROMPT)
    summary = summarizer.generate_text(context)
    self.current_summary = summary

    # Sauvegarde de la conversation
    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{date}-conversation.json"
    with open(filename, 'w') as f:
      json.dump(self.long_history, f)

  def get_recent_context(self):
    
    context = f"Résumé de la conversation: {self.current_summary}\n" 
    for msg, resp in self.recent_history:
      context += f"Utilisateur: {msg}\nSynergi: {resp}\n"
    
    context += f"Buts de la conversation: {self.conversation_goals}\n"
    context += "Synergi: "  
    return context