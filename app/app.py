import os
import shutil
import json
from template_Functions import SettingFunctionsClass
from utils import ColorPrint, ErrorPrint

# Variables

running_state = {"running": True} # This makes it so it will stop running if the user chooses to exit or there is a major error.

SettingFunctions = SettingFunctionsClass() # This gets the Functions that the TemplateOptions use, e.g. ChangePort which is used by all the Default Templates.
TemplateOptions = {} # These are what options each template has, e.g. Change Port, and assigns the function ChangePort to it.

def NuminRange(num, list): # e.g if the user inputs 1 out of 5 options it will return True, if not it will return False
    index = num-1
    if index in range(0, len(list)):
        return True
    else:
        return False
    
def ColorInput(inputText, color): # A input with a color
    ColorPrint(inputText, color)
    inpt = input()
    return inpt

def QueryManager(Querylist, inputText): # Prints a numbered list of all the Options and allows the user to pick a option using a number
    for i, element in enumerate(Querylist):
        print(f"{i+1}. {element}")

    InitialText = f"{inputText} Enter a number between 1 and {len(Querylist)} "
    ErrorText = f"Invalid input, please enter a number between 1 and {len(Querylist)} "
    num = int(ColorInput(InitialText, "purple"))

    while not NuminRange(num, Querylist):
        num = int(ColorInput(ErrorText, "red"))

    index = num-1
    return index

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # The directory of app.py, this is to get the Templates folder and TemplateOptions.json, without this you could only run this inside of the app directory
TemplateOptionsPath = os.path.join(BASE_DIR, "TemplateOptions.json")

with open(TemplateOptionsPath, "r") as f: # Turns the TemplateSettings.json into a usable object to access what options the user can use
    TemplateOptions = json.load(f)

def main(): # The main function, this is just for the package version

    name = input("Enter the name of the Project: ").strip()
    

    templates_path = os.path.join(BASE_DIR, "templates") # The path of Templates
    templates = os.listdir(templates_path) # The name of the folders indside of Templates, so the templates

    templateIndex = QueryManager(templates, "Choose a template from the list above.") # The index of what template you chose, so if it is the first one, it would be 0
    TemplateType = templates[templateIndex] # Gets the name of the Template
    source_folder = os.path.join(templates_path, TemplateType) # Gets the folder of the chosen template
    destination_parent = os.getcwd() # The path is where app.py is run from and where the Copy of the template will go to 

    destination_folder = os.path.join(destination_parent, name) # The path of the new Folder
    shutil.copytree(source_folder, destination_folder) # Copies the chosen folder with the new name and the directory

    if input(f"Would you like to Change some settings of {name}? (Y/N) ").upper() != "Y": # If you would like to continue with some settings
        return 

    while running_state["running"]: # While the user has not exited or there was not a major error

        Options = TemplateOptions.get(TemplateType) # Gets all of the Options for the chosen Template, this is editable in TemplateOptions.json
        if Options: # If they exist
        
            OptionsKeys = list(Options.keys()) # The name of each Option, e.g. "Change Port", "Exit"

            index = QueryManager(OptionsKeys, "Choose what you want to edit.") # Gets the index of what option you want to do, e.g. Option 1 Chane Port the index would be 0
            FunctionName = Options[OptionsKeys[index]] # Gets the name of the function connected to the Option, e.g "Change Port" would get "ChangePort" function

            func = getattr(SettingFunctions, FunctionName, None) # Gets the actual function from the name and from template_Functions.py

        
            if not callable(func): # If the function does not exist 
                ErrorPrint(
                    f"Function '{FunctionName}' not found in template_Functions.py"
                )
                continue

            if FunctionName != "Exit": # If the function is not exit then it adds the templateType and the path of the new Folder
                func(TemplateType, destination_folder)
            else:
                func(running_state) # Exits the program by changing the Running state
        else:
            
            ErrorPrint(f"No Options found for {TemplateType}, if this is a custom Template make sure to add a settings to TemplateSettings.json.")
            SettingFunctions.Exit(running_state)

    ColorPrint("Bye bye!", "red")

if __name__ == "__main__":
    main()
