#json 
import json
from llms.llms import Model
from datetime import datetime
from  state_looker.state import StateLookup
import redis
class Orchestrator :
     def __init__(self):
     self.state=StateLookup()

     def self_guided_actions():
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
        date = datetime.now().strftime("%Y-%m-%d")
        #Time in this format 12:00
        time = datetime.now().strftime("%H:%M")
        username=self.state.username
        goals=self.state.user_goals
        actions=self.state.recent_actions
        productivity_stat=self.state.productivity_stat
        agenda=self.state.agenda
        metrics=self.state.important_metrics
        improvement_areas=self.state.improvement_areas
        score_board=self.state.score_board
        prompt="""
           Today is {date} and the time is {time} 

            I am an autonomous agent with capabilities to interact with the {platform} environment who i am executed , the user, the web, databases and file systems. I have multiple tools to be highly efficient and to decuplate my capacity.  

            The user I am assisting is {username}. Their current goals are: {goals}

             Some recent actions I have taken include:{actions}

             Their productivity statistics show:{productivity_stat}

             Looking at their agenda, they have the following meetings/commitments today:{agenda}

             Metrics to monitor are:{metrics}

             I should focus on improving {improvement_areas} based on previous feedback.

             My current score board is: {score_board}. I aim to improve it by taking high-impact actions tailored to the user's context.

              Given all this, generate a structured plan of actions to take today to provide maximum value to {username} and be the best assistant. Ensure the plan considers their goals, previous actions, productivity, agenda and areas to improve. 
           """
        prompt=prompt.format(platform=self.state.my_os ,date=date,time=time,username=username,actions=actions,productivity_stat=productivity_stat,metrics=metrics,improvement_areas=improvement_areas,score_board=score_board)
        
        prompt +="""The plan should be a JSON object with fields:
                   {
                     "actions": [
                       {
                    "description": "Action description",
                    "interval": "Time interval"
                   },
                 ]
                }"""
        model = Model("gpt3", master_prompt=prompt, api_key="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")
        plan=model.generate_text("the json:")
        plan=extract_json(plan)
        return plan 
     def generatate_autonomous_planning():


     def 