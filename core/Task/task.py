from datetime import datetime

class Task:
    def __init__(self, description, due_date=None):
        self.description = description
        self.due_date = due_date
        self.subtasks = []
        self.status = 'Not started'

    def run(self):
        # Exécute la tâche en appelant les sous-tâches
        for subtask in self.subtasks:
            subtask.run()

        # Marque la tâche comme terminée
        self.mark_done()

    def add_subtask(self, task):
        # Ajoute une sous-tâche
        self.subtasks.append(task)

    def mark_done(self):
        # Marque la tâche comme terminée
        self.status = 'Done'

class Scheduler:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        # Ajoute une tâche à la liste des tâches
        self.tasks.append(task)

    def schedule(self, date):
        # Planifie l'exécution des tâches à une date donnée
        for task in self.tasks:
            if task.due_date == date:
                task.run()

# Exemple d'utilisation
task1 = Task('Tâche 1', datetime(2022, 12, 31))
subtask1 = Task('Sous-tâche 1')
subtask2 = Task('Sous-tâche 2')
task1.add_subtask(subtask1)
task1.add_subtask(subtask2)

task2 = Task('Tâche 2', datetime(2022, 12, 31))
subtask3 = Task('Sous-tâche 3')
subtask4 = Task('Sous-tâche 4')
task2.add_subtask(subtask3)
task2.add_subtask(subtask4)

scheduler = Scheduler()
scheduler.add_task(task1)
scheduler.add_task(task2)

scheduler.schedule(datetime(2022, 12, 31))