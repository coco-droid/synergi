import datetime
from productivity.productivity import ProductivityAnalyzer
import platform


class StateLookup:

    def __init__(self):
        #init redis local database
        self.redis = Redis(host='localhost', port=6379, db=0) 
        self.my_os=platform.system()
        self.user_goals
        self.recent_actions
        self.productivity_stat
        self.agenda
        self.important_metrics
        self.improvement_areas
        self.score_board
    def update_variable(self):
        self.score_board=self.get_score_board()
        self.user_goals=self.get_user_goals()
        self.recent_actions=self.get_recent_actions()
        self.productivity_stat=self.get_productivity_stats()
        self.agenda=self.get_agenda()
        self.important_metrics=self.get_important_metrics()
        self.improvement_areas=self.get_improvement()

    def get_user_goals(self, user_id):
        #get reecent goals on the user_goal is a object with the goal 
        #and the date it was created
        goal=self.redis.get('user_goal')
        #get the five last goal in the goal array 
        goals=goal[-5:]
        return goals

    def get_recent_actions(self, user_id):
        return actions

    def get_productivity_stats(self, user_id):
        return stats

    def get_agenda(self, user_id):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        agenda=self.redis.get('user_agenda')
        #get the agenda for the day in agenda object 
        agenda=agenda[today]
        return agenda

    def get_preferences(self, user_id):
        return preferences
    def get_score_board(self):

    def get_ameliorate_point(self):
        return point 

    def get_important_metrics(self):        
        return metrics
    def getPersonnalInfo(self):
        return self.redis.get('personnal_info')
    def establish_profile(self):
        user=self.getPersonnalInfo()
        old_p=self.redis.get('the_user_desc')
        profiler=self.redis.get('profiler_ai')
        info_p=''
        for info in profiler:
            info_p=info+"\n"
        prompt="""you are a profiler agent your mission is to establish a profile of the user 
        use this extracted insight on conversation to create a profile of the user :\n
        {info_p}
        and other additional information like
         age:{age}
         Gender:{gender}
         marital:{marital}
        the old user profile{old_p}
        """
        prompt=prompt.format(age=age,gender=gender,marital=marital,info_p=info_p,old_p=old_p)
        #update 
        self.redis.set('the_user_desc',prompt)