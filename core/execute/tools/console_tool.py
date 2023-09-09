# tools/console_tool.py

import subprocess

def console_tool(command):
    print(command)
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        print(output)
        return output
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e}"
