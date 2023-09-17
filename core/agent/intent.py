import json
from json import JSONDecodeError
import re
from llms.llms import Model
#from memory.episodic import EpisodicMemory
from agent.contextual import ContextConversation
from execute.tools.apps_launcher_tool import apps_launcher_tool
from datetime import datetime
PROMPT_PREDICT_KEYS = """
En vous basant sur le contexte conversationnel fourni, prédire une liste de 1 à 5 clés candidates dans la mémoire épisodique pouvant être pertinentes:
"""

class IntentAnalyzer:

    def __init__(self):

        #self.episodic_memory = EpisodicMemory('synergi_index') 
        self.context = ContextConversation()
        self.key_predictor = Model("gpt3", prompt=PROMPT_PREDICT_KEYS, api_key="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")

    def predict(self, message):
        def extract_json(text):
            print("the init")
            print(text)
            start_index = text.index('{')
            end_index = text.rindex('}') + 1
            # Extract the JSON substring
            json_string = text[start_index:end_index]
            # Parse the JSON string into a Python dictionary
            try:
                json_obj = json.loads(json_string)
                return json_obj
            except json.JSONDecodeError:
                print("oops no json!")
                return {
                    "intent": "greet",
                    "output": "I'm doing well, thanks for asking! How can I help you today?",
                    "action": None,
                    "goal": None,
                    "steps": [],
                    "predicted_keys": []
                }

        date = datetime.now().strftime("%Y-%m-%d")
        #Time in this format 12:00
        time = datetime.now().strftime("%H:%M")
        #a summary of the conversation
        summary=self.context.long_summary
        username="Robert"
        #recent messages
        recent_messages =self.context.recent_summary
        json_samples =  '''
          "intent": "The message's goal",
          "synergi_say": "Reply thoughtfully, with empathy, wisdom and wit. Weave in humor when suitable. Show you grasp the full context. Provide advice from a place of benevolence. Demonstrate intellect and creativity in elevating discourse. Above all, respond as the caring, cultured and warm-hearted friend of {username}.
            For example, you might write: 'I can understand why you feel that way. Here's my perspective on the situation and some options I recommend exploring...' make the conversation flow naturally like humans do.",
          "action": "Describe the helpful actions to execute when the user demand  ",
          "goal": "A complex task to do for the user ",
          "goal_details": "Tips for achieving the goal",
          "lauch_app": "if user want to open a apps ",
          "get_episodic_data": "Keywords for relevant memories.",
          "set_episodic_mem": "To store helpful memories",
          '''
        json_samples=json_samples.format(username=username)
        json_samples="{\n"+json_samples+"\n}" 
        master_prompt = '''You are Synergie, the virtual friend of {username}. Your purpose is having natural conversations to understand, assist and guide them kindly. You are empathetic, wise, creative and humorous when suitable.

For example, if {username} shares about having a bad day, you might respond: "I'm sorry to hear you had such a rough day. It's completely understandable to feel frustrated when things don't go as planned. Tomorrow is a new day - let me know if you need help figuring out how to approach it differently."

Today is {date}. The time is {time}. You have access to the conversation summary {summary} and recent messages {recent_messages} to provide relevant context.

When {username} sends a message, infer its intent, 
YOU MUST BE RETURN A JSON LIKE THIS:
{json_samples} 
'''
        #format
        master_prompt = master_prompt.format(date=date, time=time, username="Robert", summary=summary, recent_messages=recent_messages, json_samples=json_samples)
        model = Model("gpt4-clarifai", master_prompt=master_prompt, api_key="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")
        user_message =username+"say:"+message+"\nsynerige_json_response:"
        response = model.generate_text(user_message)
        print(response)
        data = extract_json(response)

        if "lauch_app" in data and data["lauch_app"] != None and data["lauch_app"] != "":
            #apps_launcher_tool(data["lauch_app"])
            pass
                #self.episodic_memory.save(element, key) 

        #function to delete all null key in data
        data = {k: v for k, v in data.items() if v is not None}
        print(f"IntentAnalyzer: {data}")

        #save output in context
        self.context.update('',data["synergi_say"])
        return data