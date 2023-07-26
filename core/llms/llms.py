import os
import openai
from llms.jurassic import Jurassic
from langchain.chat_models import ChatAnthropic, ChatOpenAI
from langchain.schema import AIMessage, HumanMessage  
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate

class Model:

  MODELS = {
    'claude': ChatAnthropic,
    'gpt4': ChatOpenAI,
    'gpt3': ChatOpenAI, 
    'jurassic': Jurassic
  }

  def __init__(self, model_name, **kwargs):
    self.model_name = model_name
    
    if model_name.lower() in self.MODELS:
      model_class = self.MODELS[model_name.lower()]

      if model_name.lower() == 'claude':
        self.model = model_class(model='claude-2')

      elif model_name.lower() == 'jurassic':
        self.model = model_class(kwargs['api_key'])
      
      elif model_name.lower() in ['gpt3', 'gpt4']:
        #openai.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = kwargs['api_key']
        self.model = model_class(
          model=model_name,
          temperature=0
        )

    else:
      raise ValueError(f"Invalid model name: {model_name}")

    self.master_prompt = kwargs.get('master_prompt', None)

  def generate_text(self, user_input):

    prompt = user_input
    if self.master_prompt:
      prompt = f"{self.master_prompt} {prompt}"
    
    try:
      if self.model_name.lower() == 'jurassic':
        response = self.model.generate(prompt)  

      elif self.model_name.lower() == 'claude':
        messages = [HumanMessage(content=prompt)]
        response = self.model.predict_messages(messages)[0].content

      elif self.model_name.lower() in ['gpt3', 'gpt4']:
        response = self.model.generate(
          prompt=prompt,
          max_tokens=100,
          temperature=0.7
        )

    except Exception as e:
      print(f"Error: {e}")
      return "Désolé, erreur lors de la génération de texte."

    return response