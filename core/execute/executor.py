import json
import importlib
import logging
import os
import datetime
from llms.llms import Model
import re
import sys
# join tools module directory
#dirname for list_tools.json

dirname = os.path.dirname(__file__)
tools_config_file = os.path.join(dirname, "list_tools.json")
tools_module_path= os.path.join(dirname,"tools")
sys.path.append(tools_module_path)

class Executor:
    def __init__(self):
        self.action_chain = []
        self.tools_config = self.load_tools_config(tools_config_file)
        self.logger = logging.getLogger("Executor")
        self.logger.setLevel(logging.DEBUG)
        # Add handlers and formatting as needed

    def generate_comprehensible_tools_list(self):
        print("Generating comprehensible tools list")
        # Generate a description of the tools list for the natural language model
        tools_list = self.load_tools_config(tools_config_file)
        tools_list_description = ""
        for tool_name, tool in tools_list.items():  # Use .items() to unpack key-value pairs
            print(f"Tool: {tool_name} data: {tool}")
            # Format like a table with this format: | tool name | tool description | tool parameters |
            tools_list_description += f"{tool_name}\n"
            for param in tool['parameters']:
                tools_list_description += f" | {param['name']} | {param['description']}|\n"
            print(f"Tools list description: {tools_list_description}")
        return tools_list_description

    def load_tools_config(self, config_file):
        with open(config_file, "r") as file:
            tools_config = json.load(file)
        return tools_config

    def validate_task(self, task):
        print(task)
        if "title" not in task:
            raise TaskValidationError("Task must have a title")
        # ... Other validation checks

    def validate_action(self, action):
        if "tool" not in action:
            raise ActionValidationError("Action must have a tool")
        # ... Other validation checks

    def execute(self, task):
            self.validate_task(task)

            if not self.check_dependencies(task):
                raise DependencyError("Dependency check failed")

            if task["method"] == "sync":
                print(f"Executing task '{task}' synchronously {task['description']}")
                actions = self.decompose(task["description"])
                print(f"Actions: {actions}")
                for i, action in enumerate(actions):
                    print(f"Validating action {i}: {action}")
                    self.validate_action(action)
                    tool_name = action["tool"]
                    tool_params = action["params"]

                    # If the action depends on a previous action's output
                    if  "depends_on" in action:
                        print("Depends on previous action")
                        dependency_index = action["depends_on"]
                        if dependency_index < i:
                            print("Dependency already executed")
                            print(self.action_chain[dependency_index]["output"])
                            dependency_output = self.action_chain[dependency_index]["output"]
                            tool_params[action["field_depends_on"]] = f"{dependency_output}"
                    print(f"Executing action {i}: {tool_name} with params {tool_params}")
                    action_output = self.execute_action(tool_name, tool_params)
                    self.action_chain.append({"action": action, "output": action_output})
            else:
                # Handle async execution
                pass

            return self.action_chain



    def check_dependencies(self, task):
        # Implement dependency check logic here
        return True

    def execute_action(self, tool_name, params):
        print(f"Executing action: {tool_name} with params: {params}")
        if tool_name in self.tools_config:
            print(f"Executing tool '{tool_name}' with params: {params}")
            tool_config = self.tools_config[tool_name]
            print(f"Tool config: {tool_config['file']}")
            tool_module = importlib.import_module(f"execute.tools.{tool_config['file']}")
            tool_function = getattr(tool_module, f"{tool_name}_tool")
            tool_output = tool_function(**params)
            print(f"Tool '{tool_name}' output: {tool_output}")
            return tool_output
        else:
            raise ToolNotFoundError(f"Tool '{tool_name}' not found in config")

    def decompose(self, description):
        print(f"Decomposing task description: {description}")
        # information about the OS configuration and time and date 
        OS_information =f"Operating System Type: Linux (KDE) date and time: {datetime.datetime.now()}"
        prompt='''I am an AI assistant that decomposes complex tasks into execution plans.
Generate the list of actions to execute this task and return a json like this:
{
"actions": 
[
{
"tool": "name of the  tool to use",
"params": {...},
"depends_on": index of the action on which this one depends don't return if no dependency
"field_depends_on": name of the parameter that will receive the result don't return if no dependency
},
...
]
}
I take into account the operating system:linux kde  on which I am to refine my answer
Each action must specify:

The tool to use
Its parameters use the description to generate the correct values for the parameters Operating System Type: Linux (KDE) 
Its dependencies on other actions:
"depends_on": index of the action on which this one depends
"field_depends_on": parameter that will receive the result
Analyze the task description semantically to generate a coordinated action plan.'''
        prompt +="\n"+OS_information+"\n"
        prompt += f"List of available tools you can use: {self.generate_comprehensible_tools_list()}\n"
        # Call LLMS to decompose description into actions
        # Returns a list of action objects
        summarizer = Model("gpt3", master_prompt=prompt, api_key="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")
        context=f"Given:A task description in natural language:{description}"
        print(f"Context: {context}")
        summary = extract_json(summarizer.generate_text(context))
        print(f"Summary: {summary}")
        return summary["actions"]

    

class TaskValidationError(Exception):
    pass

class ActionValidationError(Exception):
    pass

class DependencyError(Exception):
    pass

class ToolNotFoundError(Exception):
    pass

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


