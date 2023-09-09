from llms.llms import Model 
from  state_looker.state import StateLookup
class  CoachingAssistant:
    def __init__(self)
       self.state=StateLookup()
    def coaching(self,message):
        #initialize the variable
        personnal_info=self.state.getPersonnalInfo()
        age=personnal_info['age']
        gender=personnal_info['gender']
        marital_status=personnal_info['marital_status']
        goals=
        more_contextual_info=
        prompt=""""You are a coaching agent, your mission is to help user {user_id} achieve his goals. According to the information in your databases:

The user is a {age}-year old {gender}, who is {marital_status} her goals {goal} and this additionnal information:{additional}

Generate a coaching insight to give a chatbot to coach the user return a json like this :
"
    """
        prompt=prompt.format(age=age,gender=gender,marital_status=marital_status,goal=goals,additional=more_contextual_info)
        prompt +="""
        {
           coach:[]
        }
        """
        model = Model("gpt3", master_prompt=prompt, api_key="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")
        response=model.generate_text('the json you return:')
        response=extract_json(response)
        return response