import os
import json
from datetime import datetime
import redis
from llms.llms import Model

# Initialize Redis connection
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# set path to the conversation folder
SUMMARY_FREQUENCY = 5
MIN_HISTORY = 5
# the prompt to summarize the conversation and keep the context and important information
SUMMARIZE_PROMPT = "Summarize this conversation to keep the context and important information:"
class ContextConversation:

    def __init__(self):
        self.recent_history = []
        self.long_history = []
        self.conversation_goals = ""
        self.long_summary = "The conversation is starting"
        self.recent_summary = "There is no recent messages"
        self.no_summary_count = 0
        #self.conversation_file = self.get_conversation_filename()
        #self.all_history_file = os.path.join(CONVERSATIONS_DIR, "all_history.json")

    def save_conversation(self):
        data = {
            "long_history": self.long_history,
            "conversation_goals": self.conversation_goals,
            "summary": self.long_summary
        }
        conversation_key = self.get_conversation_key()
        redis_client.set(conversation_key, json.dumps(data))
        self.update_all_history()

    def retrieve_conversation(self):
        conversation_key = self.get_conversation_key()
        conversation_data = redis_client.get(conversation_key)
        if conversation_data:
            data = json.loads(conversation_data)
            self.long_history = data["long_history"]
            self.conversation_goals = data["conversation_goals"]
            self.long_summary = data["summary"]
    def update(self, message, response, message_type="text"):
        if message.strip():
            # Mettre à jour les historiques
            self.recent_history.append({"emettor": "user", "message": message, "type": message_type})
            self.long_history.append({"emettor": "user", "message": message, "type": message_type})
        elif response.strip():
            self.long_history.append({"emettor": "bot", "message": response, "type": "text"})
            self.recent_history.append({"emettor": "bot", "message": response, "type": "text"})
        else:
          print('Nothing..')
        
        if len(self.recent_history) > 10:
            self.recent_history = self.recent_history[-10:]
            self.long_history.append({"emettor": "user", "message": message, "type": message_type})
            self.long_history.append({"emettor": "bot", "message": response, "type": "text"})
            # Compteur pour savoir quand régénérer résumé
            self.no_summary_count += 1
        print(f"recent_history: {len(self.recent_history)}")
        if  len(self.recent_history) >= 10:
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

            summarizer = Model("jurassic", master_prompt=SUMMARIZE_PROMPT, api_key="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")
            summary = summarizer.generate_text(context)

            self.long_summary = summary
        else:
            self.long_summary = "a simple conversation"
    def regenerate_recent_summary(self):
        summary = "Recent messages:\n\n"
        #five last messages in recent history
        recent_history = self.recent_history[-5:]
        for item in recent_history:
            if item["emettor"] == "user":
                summary += f"Old User message: {item['message']}\n"
            elif item["emettor"] == "bot":
                summary += f"Old Synergi message: {item['message']}\n"
        self.recent_summary = summary
    def get_recent_context(self):
        context = f"Summary of conversation: {self.long_summary}\n"
        context += f"Recent messages: {self.recent_summary}\n"
        context += f"Conversation goals: {self.conversation_goals}\n"
        return context    
    # ... Your other methods ...
    def get_conversation_key(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return f"conversation_{today}"
    def get_conversation_dates(self):
        return self.load_all_history()
    def load_all_history(self):
        if redis_client.exists("all_history"):
            all_history_data = redis_client.get("all_history")
            return json.loads(all_history_data)
        return []
    def retrieve_all_history(self):
        all_history = self.load_all_history()
        return all_history
    def get_conversation(self, date):
        conversation_key = self.get_conversation_key_for_date(date)
        conversation_data = redis_client.get(conversation_key)
        if conversation_data:
         return json.loads(conversation_data)
        return None
    def get_conversation_key_for_date(self, date):
        return f"conversation_{date}"
    def update_all_history(self):
        all_history = self.load_all_history()
        today_date = datetime.now().strftime("%Y-%m-%d")

        # Check if an entry with today's date already exists, and update it if it does
        for entry in all_history:
            if entry["Date"] == today_date:
                entry["summary"] = self.long_summary
                break
        else:
            summary_entry = {
                "summary": self.long_summary,
                "Date": today_date
            }
            all_history.append(summary_entry)

        redis_client.set("all_history", json.dumps(all_history))
    def get_today_conversation_on_redis(self):
        conversation_key = self.get_conversation_key()
        conversation_data = redis_client.get(conversation_key)
        if conversation_data:
            return json.loads(conversation_data)
        return None
    def delete_today_conversation_on_redis(self):
        conversation_key = self.get_conversation_key()
        redis_client.delete(conversation_key)
    def delete_date_conversation_on_redis(self,date):
        conversation_key = self.get_conversation_key_for_date(date)
        redis_client.delete(conversation_key)
        #delete the date field in the all_history
        all_history = self.load_all_history()
        for entry in all_history:
            if entry["Date"] == date:
                all_history.remove(entry)
                break
        redis_client.set("all_history", json.dumps(all_history))
        
#test the contextual conversation
