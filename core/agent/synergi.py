from agent.intent import IntentAnalyzer
from memory.episodic import EpisodicMemory
from memory.procedural import ProceduralMemory
from execute.executor import Executor
import os
from Task.task import Task
from TTS.speech import Speech
import sys

class SynergiAgent:
  def __init__(self):
      self.intent_analyzer = IntentAnalyzer()
      self.execute_action = Executor()
      self.episodic_memory = EpisodicMemory('synergi')
      self.procedural_memory = ProceduralMemory()
    

  def handle_message(self,message,websocket):
      print(f"intent analyzer: {self.intent_analyzer}")
      data = self.intent_analyzer.predict(message)

      # Actions synchrones simples 

      # Actions synchrones simples 
      if "action" in data and data["action"] != None and data["action"] != "":
        self.execute_action.execute({'title':'A simple action','description':data["action"],'method':'sync'})
        pass # Add a placeholder statement here

      # Récupérer mémoire épisodique
      if "predicted_keys" in data and data["predicted_keys"] != None and data["predicted_keys"] != "":
        #memories = self.episodic_memory.retrieve(data["predicted_keys"])
        # Faire quelque chose avec les mémoires récupérées
        pass # Add a placeholder statement here

      # Mémorisation épisodique
      if "memorize" in data:
        for element in data["memorize"]:
          #key = generate_key()
          #self.episodic_memory.save(element, key)
          pass # Add a placeholder statement here

      # Tâches asynchrones complexes
      if "goals_detailed" in data :
        #task=Task(data["goal"],data["goals_detailed"])
        pass 
      test1=Speech(data["synergi_say"],'local')
      test1.play_audio()
      return data["synergi_say"]
   