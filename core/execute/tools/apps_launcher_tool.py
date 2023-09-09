import os
import platform
import pathlib
import subprocess
import json
from llms.llms import Model

def apps_launcher_tool(description):
    def removeExtension(name):
        return os.path.splitext(name)[0]
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
    def get_installed_apps(os):
        apps = []

        if os == "Linux":
            # Récupère les .desktop dans les répertoires d'applications
            app_dirs = ["/usr/share/applications", "/var/lib/snapd/desktop/applications"]
            for app_dir in app_dirs:
                for entry in pathlib.Path(app_dir).iterdir():
                    if entry.suffix == ".desktop":
                        apps.append(entry.name)

        elif os == "Windows": 
            # Récupère les logiciels de la registry
            result = subprocess.run(["powershell", "Get-ItemProperty HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName"], capture_output=True)
            for line in result.stdout.decode().splitlines():
                app = line.split()[-1]
                apps.append(app)

        elif os == "Darwin":
            # Récupère les .app du répertoire Applications
            for entry in pathlib.Path("/Applications").iterdir():
                if entry.suffix == ".app":
                    apps.append(entry.name)

        return apps

    #to get the os if is linux, windows or macos
    my_os = platform.system()
    #parse my_os to get if is linux,windows or macos

    #list of installed apps 
    apps = get_installed_apps(my_os)
    print(apps)
    #master prompt to indicate the large language model gpt3.5 to find the app to lauch 
    master_prompt = f"Use this list of installed apps:{apps} to choose the apps corresponding with the description i will take you rerun a json like this:"
    master_prompt +='{"app":[name list of apps corresponding with the description]}'
    #to use the llms to find the app to lauch with the desc
    find_app = Model("gpt3", master_prompt=master_prompt, api_key="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")
    app = find_app.generate_text(f"Description of the app:{description}\n json response:")
    #to lauch the app
    app = extract_json(app)['app']
    #remove extention .dekstop, .exe etc... in the name of application 
    os.system(removeExtension(app[0]))
    print(f"Lauching {app}")
    return f"Lauching {app}"


