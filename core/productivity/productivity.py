import json 
import redis
from llms.llms import Model 
import coaching
import stress_management
from datetime import datetime, timedelta

# Initialisation Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

class ProductivityAnalyzer:

  def __init__(self):
    self.coach = coaching.CoachingAssistant()
    self.stress_mgr = stress_management.StressManager()
    self.date = datetime.now().strftime("%Y-%m-%d")

  def analyze(self, user_data):
    # Receive a user message and analyze it to extract routines and goals
    prompt = """
      I have recent posts from a user named {name}. Semantically analyze these messages to infer information about {name}'s routines, habits, and productivity patterns.

      The messages are as follows:

      {posts}

      Generate a textual description of detected routines, such as recurring meetings, regular activities, usual productivity time slots.

      Also provide relevant statistics and measures identified, such as the average duration of certain tasks.

      Insight: Structure the inferred information into coherent short sentences describing detected routines and productivity statistics.

      Include only relevant information supported by message data. Ignore details unrelated to productivity and routines.
    """
    prompt = prompt.format(name=name, posts=message)
    prompt += """
      return a json 
      {
        "routine": routine extracted from the user message,
        "goals": goals extracted from the user message,
        "metrics": some metrics about her productivity extracted from the user message,
        "insight": some insight extracted from the user message
      }
    """
    model = Model("gpt3", master_prompt=prompt, api_key="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")
    response = model.generate_text('the json:')
    self.save_on_records(response)

  def save_on_records(self, res):
    # Retrieve the productivity insight db
    old = redis_client.get("productivity_insight")
    if old:
      old = json.loads(old)
      date = datetime.now().strftime("%Y-%m-%d")
      old[date] = []
      old[date].append(res)
      redis_client.set("productivity_insight", json.dumps(old))
    else:
      redis_client.set("productivity_insight", json.dumps({date: [res]}))

  def get_insight(self):
    # Retrieve the productivity insight db
    old = redis_client.get("productivity_insight")
    if old:
      old = json.loads(old)
      date = datetime.now().strftime("%Y-%m-%d")
      return old[date]
    else:
      return None

  def get_insight_date(self, date):
    # Retrieve the productivity insight db
    old = redis_client.get("productivity_insight")
    if old:
      old = json.loads(old)
      return old[date]
    else:
      return None

  def get_productivity_map(self, date):
    # Retrieve the productivity insight db
    old = redis_client.get("productivity_map")
    if old:
      old = json.loads(old)
      return old[date]
    else:
      return None

  def analyse_insight_data(self):
    today_insight = self.get_insight()
    if today_insight:
      # Get the previous day's productivity_map
      yesterday = datetime.now() - timedelta(days=1)
      yesterday = yesterday.strftime("%Y-%m-%d")
      yesterday_map = self.get_productivity_map(yesterday)
      if yesterday_map:
        prompt = """
          You are a productivity enhancer. To accomplish your work, you have the following:

          Today's productivity insight: {today_insight}
          Yesterday's productivity resume: {yesterday_map}
          The agenda of the user for today: {agenda}
          The user's goals: {goals}

          You may return a productivity score, routine adherence, task accomplishment today, and other metrics like time users are more productive, deducted recreational time, etc.
        """
        prompt = prompt.format(today_insight=today_insight, yesterday_map=yesterday_map, agenda=agenda, goals=goals)
        model = Model("gpt3", master_prompt=prompt, api_key="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")  
        response = model.generate_text('the json:')
        self.save_the_map(response)

  def generate_metrics(self):
    # Number of tasks accomplished in the day, time spent on each task, number of pauses per day, productivity sentiment, level of exhaustion
    agenda = redis_client.get("user_agenda")
    goals = redis_client.get("user_goals")
    # Get insight of the day to get exhaustion level
    days_insight = self.get_insight()
    fatigue = 0
    accomplish = 0
    if days_insight:
      for insight in days_insight:
        if insight["fatigue"] == "fatigue":
          fatigue += 1
        else:
          fatigue -= 1
    if fatigue == 1 or fatigue == 2:
      fatigue = "faible"
    elif fatigue == len(days_insight) - 2:
      fatigue = "medium"
    else:
      fatigue = "elevate"
    if agenda[self.date]:
      for task in agenda[self.date]:
        if task["accomplish"]:
          accomplish += 1
        else:
          accomplish = accomplish
    # Generate metrics 
    metrics = {
      "accomplish": accomplish,
      "fatigue": fatigue
    }
    #self.coach.coaching(metrics)