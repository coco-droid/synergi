import os
import subprocess
from llms.llms import Model
from memory.procedural import ProceduralMemory

class Executor:

  def __init__(self, websocket):
    self.websocket = websocket
    self.os = self.detect_os()
    self.procedural_memory = ProceduralMemory()

  def detect_os(self):
    import platform
    return platform.system() 

  def execute(self, action, send_response=False):
    
    if self.procedural_memory.exists(action["tool"]):
      return self.procedural_memory.execute(action["tool"], action["params"])

    try:
      if action["tool"] == "app":
        return self.launch_app(action["name"])

      if action["tool"] == "bash":
        return self.bash_execute(action["command"])

      if action["tool"] == "search":
        return self.web_search(action["query"])

      # etc...

    except Exception as e:
      if send_response:
        error_msg = self.generate_error_response(action, e)
        self.websocket.send(error_msg)

  def launch_app(self, name):
    if self.os == "Windows":
      os.startfile(name)
    else:  
      os.system(f"open {name}")

  def bash_execute(self, command):
    return subprocess.check_output(command, shell=True)

  def web_search(self, query):
    # Code de recherche web
    return results

  def teach(self, name, function):
    self.procedural_memory.insert(name, function)

  def execute_taught_procedure(self, name, params):
    return self.procedural_memory.execute(name, params)

  