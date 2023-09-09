#from llms.llms import Model
#from datetime import datetime
#from agent.contextual import ContextConversation
#from execute.executor import Executor
#conversation = ContextConversation()
#conversation.retrieve_conversation()
#simulate a real conversation 
#usersend message:conversation.update("hello", "")
#botsend message:conversation.update("", "hello")
#conversation.update("hello", "")
#conversation.update("", "hello")
#conversation about a story and a question
#
#conversation.update("okay, can you tell me more about the third republic?", "")
    #retrieve the conversation
    #see the long summary
#delete today conversation 
#conversation.delete_today_conversation_on_redis()
#conversation.update("hello", "")
#conversation.update("", "hello")
#conversation.update("how are you?", "")
#conversation.update("", "I am fine, thank you")
#conversation.update("I want to know about the story of the little prince", "")
#conversation.update("", "The Little Prince, fable and modern classic by French aviator and writer Antoine de Saint-Exupery that was published with his own illustrations in French as Le Petit Prince in 1943. The simple tale tells the story of a child, the little prince, who travels the universe gaining wisdom.")
#conversation.update("okay, can you tell me more about the author?", "")
#conversation.update("", "Antoine de Saint-Exupery, French pilot and writer, born June 29, 1900, Lyon, France—died July 31, 1944, in flight over the Mediterranean) French aviator and writer whose works are the unique testimony of a pilot and a warrior who looked at adventure and danger with a poet’s eyes.")
#conversation.update("a story about a pilot?", "")
#conversation.update("", "The Little Prince is a novella by French aristocrat, writer, and aviator Antoine de Saint-Exupery. It was first published in English and French in the US by Reynal & Hitchcock in April 1943, and posthumously in France following the liberation of France as Saint-Exupery's works had been banned by the Vichy Regime.")
#conversation.update("okay, can you tell me more about vicity regime?", "")
#conversation.update("", "The Vichy regime was the French government which succeeded the Third Republic from July 1940 to August 1944. It was proclaimed by Marshal Philippe Petain following the military defeat of France and the July 10 vote by the National Assembly to grant extraordinary powers to Petain, who held the title of President of the Council.")
#print(conversation.retrieve_conversation())
#print(conversation.long_summary)
#print(conversation.recent_summary)
#execu=Executor()
#lish=execu.generate_comprehensible_tools_list()
#print(lish)
#execu.execute({"title":"a simple action","description":"open the calculator","method":"sync"})


#je veux acceder a la fonction lauch du script python ce trouvant dans /execute/tools/apps_launcher.py
from execute.tools.apps_launcher import lauch

lauch('the calculator')