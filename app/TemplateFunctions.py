#template_Functions.py

import os
from app.Utils import error_print, success_print, color_print

class SettingFunctions(): # This is a collection of all the Functions that are used in TemplateOptions.json

    def change_port(self, filetype, destination_folder): # This changes the port of a flask app, a small change 
        files = os.listdir(destination_folder)
        filename = "app.py" if "app.py" in files and not "run.py" in files else "run.py"
        if not filename:
            error_print("No app.py or run.py found in the Directory, if this is a custom template please rename the file that runs the file with either app.py or run.py")
            return 
        
        appPath = os.path.join(destination_folder, filename)
        lines = []
        with open(appPath, "r") as f:
            lines = f.readlines()

        found = False
        for i, line in enumerate(lines):
            if "app.run(" in line:
                found = True

                port = input("What port would you like to change it to? ")

                indent = line[:len(line) - len(line.lstrip())]
                lines[i] = f'{indent}app.run(host="0.0.0.0", debug=True, port={port})'
                break
        with open(appPath, "w") as f: # Re writes the file with the modified app.run line 
            f.writelines(lines)
        if not found: # if app.run has not been found in app.py or run.py
            error_print("app.run has not been found!")
        else: # If there have been no previous errors, this means it was a successful port change
            success_print("Successfully changed the Port!")


    def exit(self, running_state, *args): # This exits out of the program by changing the running State to false
        running_state["running"] = False
