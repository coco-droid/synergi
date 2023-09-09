<<<<<<< HEAD
import json
import os
from datetime import datetime
from llms.llms import Model

#get dirname 
dirname = os.path.dirname(__file__)
#set path to the conversation folder
CONVERSATIONS_DIR = os.path.join(dirname, "conversations")
SUMMARY_FREQUENCY = 5
MIN_HISTORY = 5
SUMMARIZE_PROMPT = "Summarize:"

class ContextConversation:

  def __init__(self):
    
    self.recent_history = []
    self.long_history = []
    self.conversation_goals = []
    self.long_summary = ""
    self.recent_summary = ""
    self.no_summary_count = 0
    self.conversation_file = self.get_conversation_filename()
    if not os.path.exists(CONVERSATIONS_DIR):
      os.makedirs(CONVERSATIONS_DIR)

    if os.path.exists(self.conversation_file): 
      self.retrieve_conversation()

    else:
      self.long_history = []
      self.conversation_goals = []

  def get_conversation_filename(self):
    today = datetime.now().strftime("%Y-%m-%d")
    return f"{CONVERSATIONS_DIR}/{today}-conversation.json"
  
  def save_conversation(self):
    data = {
      "long_history": self.long_history,
      "conversation_goals": self.conversation_goals,
      "summary":self.long_summary
    }
    with open(self.conversation_file, "w") as f:
      json.dump(data, f)

  def retrieve_conversation(self):
    with open(self.conversation_file, "r") as f:
      data = json.load(f)
      self.long_history = data["long_history"]
      self.conversation_goals = data["conversation_goals"]
      self.long_summary=data["summary"]

  def update(self, message, response):

    # Mettre à jour les historiques
    self.recent_history.append((message, response))

    if len(self.recent_history) > 5:
      self.recent_history = self.recent_history[-5:]

    self.long_history.append((message, response))

    # Compteur pour savoir quand régénérer résumé
    self.no_summary_count += 1
    if self.no_summary_count >= SUMMARY_FREQUENCY:
      self.no_summary_count = 0
      self.regenerate_long_summary()

    # Régénérer résumé court terme
    self.regenerate_recent_summary()
    self.save_conversation()

  def regenerate_long_summary(self):

    if len(self.long_history) >= MIN_HISTORY:
      print("Generating summary")
      history = self.long_history
      context = ""

      for msg, resp in history:
        context += f"Old User message: {msg}\n Old synergi Output key value: {resp}\n"

      summarizer =Model("jurassic", master_prompt=SUMMARIZE_PROMPT, api_key="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")
      summary = summarizer.generate_text(context)

      self.long_summary = summary
    
    else:
      self.long_summary = "a simple conversation"

  def regenerate_recent_summary(self):
    
    summary = "Recent messages:\n\n"
    for msg, resp in self.recent_history:
      if msg.strip() == "":
        pass
      else:
        summary += f"Old User message: {msg}\n"
      if resp.strip() == "":
        pass
      else:
        summary += f"Old Synergi Output key value: {resp}\n\n"
    
    self.recent_summary = summary

  def get_recent_context(self):

    context = f"Summary of conversation: {self.long_summary}\n"
    context += f"Recent messages: {self.recent_summary}\n"

    context += f"Conversation goals: {self.conversation_goals}\n"

    return context
=======
import g4f 

provider = g4f.Provider.Aichat

# Streaming is not supported by these providers
if provider in {g4f.Provider.Aws, g4f.Provider.Ora,
                g4f.Provider.Bard, g4f.Provider.Aichat}:
    stream = False
else:
    stream = True

print(provider.params)  # supported args

class SynergiAgent:
    def __init__(self):
        pass

    def handle_message(self, message):
        print(message)
        message_text = message.get('sendMessage', '') 
        response = g4f.ChatCompletion.create(model='gpt-4',
                                             messages=[{"role": "user",
                                                        "content": message_text}],
                                             stream=stream,
                                             provider=provider)

        print(response)
        return response
>>>>>>> df2b693dabb2e5532528e8c90c5b43e43824607d
