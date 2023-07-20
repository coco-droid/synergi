import os
from langchain.chat_models import ChatAnthropic, ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.llms import OpenAI

class Model:
    def __init__(self, model_name):
        self.model_name = model_name
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if model_name.lower() == 'claude':
            self.chat = ChatAnthropic(model='claude-2')
        elif model_name.lower() == 'gpt4':
            self.chat = ChatOpenAI(temperature=0)
            self.llm = OpenAI(openai_api_key=self.api_key)

    def generate_text(self, user_input):
        messages = [HumanMessage(content=user_input)]
        response = self.chat.predict_messages(messages)
        return response[0].content
