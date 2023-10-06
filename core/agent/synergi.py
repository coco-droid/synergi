from agent.intent import IntentAnalyzer
from memory.episodic import EpisodicMemory
from memory.procedural import ProceduralMemory
from execute.executor import Executor
from execute.tools.image_generator_tool import image_generator_tool
from execute.tools.docs_chat_tool import docs_chat_tool
from Task.task import Task
from TTS.speech import Speech
from queued.queued import QueueManager
import multiprocessing

redis_url = 'redis://localhost:6379/0'  # URL de votre instance Redis
queue_manager = QueueManager(redis_url)
class SynergiAgent:
    def __init__(self):
        self.intent_analyzer = IntentAnalyzer()
        self.execute_action = Executor()
        #self.episodic_memory = EpisodicMemory('synergi')
        #self.procedural_memory = ProceduralMemory()

    def _run_speech_synthesis(self, message):
        test1 = Speech(message, 'local')
        test1.play_audio()
    def run_image_generator(self,message,socketio):
        print('Trace:Image generate process')
        test = image_generator_tool(message,'dalle')
        queue_manager.publish('imagegen',{'image':test})
        
        
    def handle_message(self, message, socketio):
        print(f"intent analyzer: {self.intent_analyzer}")
        data = self.intent_analyzer.predict(message)
        # Actions synchrones simples
        if "action" in data and data["action"] is not None and data["action"] != "":
            # self.execute_action.execute({'title':'A simple action','description':data["action"],'method':'sync'})
            pass  # Add a placeholder statement here

        # Récupérer mémoire épisodique
        if "create_image" in data and data["create_image"] is not None and data["create_image"] != "":
            image_process = multiprocessing.Process(target=self.run_image_generator, args=(data['synergi_say'],''))
            image_process.daemon = True  # Make it a daemon process
            image_process.start()
            pass  # Add a placeholder statement here

        # Mémorisation épisodique
        if "memorize" in data:
            for element in data["memorize"]:
                # key = generate_key()
                # self.episodic_memory.save(element, key)
                pass  # Add a placeholder statement here

        # Tâches asynchrones complexes
        if "goals_detailed" in data:
            # task = Task(data["goal"], data["goals_detailed"])
            pass

        #print(emit)
        # Start STT process as a daemon in the background
        stt_process = multiprocessing.Process(target=self._run_speech_synthesis, args=(data['synergi_say'],))
        stt_process.daemon = True  # Make it a daemon process
        stt_process.start()
        # Continue without waiting for the STT process
        return data["synergi_say"]

    def handle_message_with_files(self, message, filename):
        test = docs_chat_tool(message, filename, 'document')
        return test
