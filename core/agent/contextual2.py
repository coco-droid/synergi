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
    self.conversation_goals = ""
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
      self.conversation_goals = ""

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

  def update(self, message, response, message_type="text"):

    # Mettre à jour les historiques
    self.recent_history.append({"emettor": "user", "message": message, "type": message_type})
    self.recent_history.append({"emettor": "bot", "message": response, "type": "text"})

    if len(self.recent_history) > 10:
      self.recent_history = self.recent_history[-10:]

    self.long_history.append({"emettor": "user", "message": message, "type": message_type})
    self.long_history.append({"emettor": "bot", "message": response, "type": "text"})

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

      for item in history:
        if item["emettor"] == "user":
          context += f"Old User message: {item['message']}\n"
        elif item["emettor"] == "bot":
          context += f"Old Synergi Output key value: {item['message']}\n"

      summarizer =Model("jurassic", master_prompt=SUMMARIZE_PROMPT, api_key="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")
      summary = summarizer.generate_text(context)

      self.long_summary = summary
    
    else:
      self.long_summary = "a simple conversation"

  def regenerate_recent_summary(self):
    
    summary = "Recent messages:\n\n"
    for item in self.recent_history:
      if item["emettor"] == "user":
        summary += f"Old User message: {item['message']}\n"
      elif item["emettor"] == "bot":
        summary += f"Old Synergi Output key value: {item['message']}\n"

    self.recent_summary = summary

  def get_recent_context(self):

    context = f"Summary of conversation: {self.long_summary}\n"
    context += f"Recent messages: {self.recent_summary}\n"

    context += f"Conversation goals: {self.conversation_goals}\n"

    return context
  #retrieve the date of conversation disponible 
  def get_conversation_dates(self):
    print('get_conversation_dates')
    dates = []
    for filename in os.listdir(CONVERSATIONS_DIR):
      date = filename.split("-")[0]
      dates.append(date)
    return dates
  #retrive the conversation of the date selected
  def get_conversation(self, date):
    print('get_conversation')
    #get the conversation file
    conversation_file = f"{CONVERSATIONS_DIR}/{date}-conversation.json"
    #open the file
    with open(conversation_file, "r") as f:
      #load the data
      data = json.load(f)
      #return the data
      return data
      