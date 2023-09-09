import redis
from datetime import datetime
from llms.llms import Model
from execute.executor import Executor
import time
import json
import re
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

class Task:

    def __init__(self, goal, details):
        self.goal = goal
        self.details = details
        self.subtasks = []
        self.executor = Executor()
        self.master_prompt = """
              Generate a list of task objects based on the given goal, details, and the goal itself.
              Generate a list of tasks return a JSON in this following format:
        {
            "tasks":
              [
               {
                "title": "Task 1",
                "description": "Description of Task 1",
                "depends_on": null,  # Index of the task it depends on (if any)
                "async": false,      # Whether the task can be executed asynchronously
                "scheduled": null   # Scheduled time for the task (if any)
               },
               {}, ...
               ]
        }
        """
        self.model = Model("gpt3", master_prompt=self.master_prompt, api_key="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")

    def generate_subtasks(self):
        print("Generating subtasks")
        resu=f"Goal: {self.goal} Details: {self.details}"
        print(resu)
        djk= extract_json(self.model.generate_text(resu))
        self.subtasks=djk['tasks']
        print(self.subtasks)
        #self.subtasks = [
          #  {
            #    "title": "Tâche 1",
            #    "description": "Description de la tâche 1",
             #   "depends_on": None,
             #   "async": False,
             #   "scheduled": None,
              #  "inputs": None,
              #  "outputs": None
           # },
           # {
               # "title": "Tâche 2",
               # "description": "Description de la tâche 2",
               # "depends_on": 0,
                #"async": True,
                #"scheduled":"2023-12-10 10:10:10",
                #"inputs": None,
                #"outputs": None
            #},
            #{
                #"title": "Tâche 3",
                #"description": "Description de la tâche 3",
                #"depends_on": 1,
                #"async": False,
                #"scheduled": None,
                #"inputs": None,
                #"outputs": None
            #}
        #]
        self.save()

    def run(self):
        self.run_async_tasks()
        self.run_sequential_tasks()
    def get_async_tasks(self):
        async_tasks = []
        for task in self.subtasks:
            if task['async'] and not task['depends_on']:
               async_tasks.append(task)
        return async_tasks
    def save_outputs(self):
        #update redis with the outputs
        self.save()
    def run_async_tasks(self):
        print("Running async tasks")
        async_tasks = self.get_async_tasks()
        for i,task in enumerate(async_tasks):
            print(f"Running async task {task['title']}")
            task["method"] = "sync"
            task['outputs'] = self.executor.execute(task) # Set the actual outputs
            #find the task in the subtasks list with her title  and update it 
            for j,subtask in enumerate(self.subtasks):
                if subtask['title'] == task['title']:
                    self.subtasks[j]['outputs'] = task['outputs']
                    break
            print(f"Task {task['title']} finished")
            self.save_outputs()

    def run_sequential_tasks(self):
        for i, task in enumerate(self.subtasks):
             if not task['async']:
                if task['depends_on']:
                   print(f"Task {task['title']} depends on {task['depends_on']}")
                   previous = self.subtasks[task['depends_on']]
                   task['inputs'] = previous['outputs']
                   task['description'] += 'Output of previous task' + previous['outputs']
                print(f"Running sequential task {task['title']}")
                task["method"] = "sync"
                task['outputs'] =  self.executor.execute(task)
                print(f"Task {task['title']} finished with output {task['outputs']}")
                self.subtasks[i]['outputs'] = task['outputs']
                self.save_outputs()

            

    def save(self):
        all_tasks = [task for task in self.subtasks]
        redis_client.set(f'task_{self.goal}', json.dumps(all_tasks))

    def add_to_scheduled(self, task):
        task_id = f"{self.goal}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        redis_client.set(f'scheduled_{task_id}', json.dumps(task))
        redis_client.sadd('scheduled_tasks', task_id)

    def load(self):
        tasks_data = redis_client.get(f'task_{self.goal}')
        if tasks_data:
            self.subtasks = json.loads(tasks_data)

    def get_task(self, goal):
        tasks_data = redis_client.get(f'task_{goal}')
        if tasks_data:
            return json.loads(tasks_data)
        return None


def run_scheduler():
    while True:
        now = datetime.now()
        scheduled_tasks = redis_client.smembers('scheduled_tasks')
        for task_id in scheduled_tasks:
            task_data = redis_client.get(f'scheduled_{task_id}')
            if task_data:
                task = json.loads(task_data)
                if task['scheduled'] < now:
                    #executor.execute(task)
                    task['outputs'] = ''  # Set the actual outputs
                    task.save_outputs()
                    redis_client.delete(f'scheduled_{task_id}')
                    redis_client.srem('scheduled_tasks', task_id)

        time.sleep(60)

def extract_json(text):
    # Trouver le JSON valide dans le texte
    match = re.search(r'({.+})', text)
    if match:
        json_str = match.group(1)

        try:
            data = json.loads(json_str)
            return data
        except JSONDecodeError:
            print("JSON invalide")

    # Sinon, tenter de parser directement tout le texte    
    try:
        data = json.loads(text)
        return data
    except JSONDecodeError:
        print("Pas de JSON valide trouvé")

    return None
def run_async():
    while True:
        async_tasks = get_async_tasks()
        for task in async_tasks:
            #executor.execute(task)
            task['outputs'] = ''  # Set the actual outputs
            task.save_outputs()

        time.sleep(60)




#if __name__ == "__main__":
    #task = Task("Faire un gâteau", "Mélanger les ingrédients")
    #task.generate_subtasks()
    #task.run()
    #task.save()
    #see = task.get_task("Faire un gâteau")
    #print('redis said:')
    #print(see)
