import os
import shutil
import json
from app.TemplateFunctions import SettingFunctions
from app.Utils import error_print, color_print

#// Variables

# Constants

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # The directory of app.py, this is to get the Templates folder and TemplateOptions.json, without this you could only run this inside of the app directory
TEMPLATEOPTIONSPATH = os.path.join(BASE_DIR, "TemplateOptions.json") # The path of TemplateOptions.json which is used to map the Options into functions from TemplateFunctions.py
TEMPLATES_PATH = os.path.join(BASE_DIR, "templates") # The path of the Templates directory
DESTINATION_PARENT = os.getcwd() # The path is where app.py is run from and where the Copy of the template will go to 

# Functions

def valid_index(num, QueryOptions): # e.g if the user inputs 1 out of 5 options it will return True, if not it will return False
    return 0 <= num-1 < len(QueryOptions)
    
def color_input(inputText, color): # A input with a color
    color_print(inputText, color)
    inpt = input()
    return inpt

def query_manager(Querylist, inputText): # Prints a numbered list of all the Options and allows the user to pick a option using a number
    for i, element in enumerate(Querylist):
        print(f"{i+1}. {element}")

    InitialText = f"{inputText} Enter a number between 1 and {len(Querylist)} "

    while True:
        try:
            num = int(color_input(InitialText, "purple"))
            if valid_index(num, Querylist):
                return num-1
        except ValueError:
            error_print("Please enter a number.")

def get_templates(template_groups):
    while True:

        template_group_index = query_manager(template_groups, "Choose what type of Template you want to make") 
        template_group = template_groups[template_group_index]
        template_group_path = os.path.join(TEMPLATES_PATH, template_group) 

        templates = os.listdir(template_group_path) 

        if not templates:
            error_print("Empty template group folder.")
            continue

        return template_group_path, list(templates)

def load_template_options(path):
    with open(path, "r") as f: # Turns the TemplateSettings.json into a usable object to access what options the user can use
        return json.load(f)
    
def merge_shortcuts(global_opts, shortcut_opts):
    for key, val in shortcut_opts.items():
        if key in global_opts and not global_opts[key]:
            global_opts[key] = val

def get_destination_folder():
    while True:
        name = input("Enter the name of the Project: ").strip()
        destination_folder = os.path.join(DESTINATION_PARENT, name)
        if not os.path.exists(destination_folder):
            return destination_folder, name
        error_print("Folder with that name already exists in this directory!")

def confirm(inputText):
    return input(inputText).strip().lower().startswith("y")

def resolve_options(template_options, template_parent, template_type, global_options, template_global_options):
    options = template_options.get(template_type, {})
    if template_parent in template_global_options:
        return {**template_global_options[template_parent], **options}
    else:
        return {**global_options, **options}

def execute_option(settings, function_name, *args):
    func = getattr(settings, function_name, None) # Gets the actual function from the name and from TemplateFunctions.py

    if not callable(func): # If the function does not exist 
        error_print(
            f"Function '{function_name}' not found in TemplateFunctions.py"
        )
        return False

    func(*args)
    return True

def main(): # The main function, this is just for the package version

    if not os.path.isdir(TEMPLATES_PATH):
        error_print("Templates folder does not exist")
        return
    if not os.path.exists(TEMPLATEOPTIONSPATH):
        error_print("TemplateOptions.json does not exist")
        return

    template_options = load_template_options(TEMPLATEOPTIONSPATH)  # These are what options each template has, e.g. Change Port, and assigns the function ChangePort to it.
    global_options = template_options.get("Global", {})
    shortcuts_options = template_options.get("Shortcuts", {})

    TemplateGlobal_options = {} # "Flask": {"Change Port": ""}
    TemplateShortcut_options = {} # "Flask": {"Change Port: """}

    #This will get the global options for templateGroups
    for key in list(template_options.keys()):
        if "-Shortcuts" in key:
            Group = key.split("-")[0]
            GroupObject = template_options[key]
            TemplateShortcut_options[Group] = GroupObject
    for TemplateKey in list(template_options.keys()):

        if "-Global" in TemplateKey:
            Group = TemplateKey.split("-")[0]
            GroupObject = template_options[TemplateKey]
            for key in GroupObject:
                if Group in TemplateShortcut_options and key in TemplateShortcut_options[Group] and GroupObject[key] == "":
                    GroupObject[key] = TemplateShortcut_options[Group][key]
                elif key in shortcuts_options and GroupObject[key] == "": # or in 'Flask-Shortcuts'
                    GroupObject[key] = shortcuts_options[key]
            TemplateGlobal_options[Group] = GroupObject

 #   for Group in TemplateShortcut_options:
 #       print(Group)
 #       if Group in TemplateGlobal_options:
 #           print("1st statment")
 #           for key in TemplateShortcut_options[Group]:
 #               print(key)
 #               print(TemplateGlobal_options[Group])
 #               if key in TemplateGlobal_options[Group] and TemplateGlobal_options[Group][key] == "":
 #                   print("passed")
 #                   TemplateGlobal_options[Group][key] = key

    merge_shortcuts(global_options, shortcuts_options)

    destination_folder, name = get_destination_folder()

    template_groups = os.listdir(TEMPLATES_PATH) # The Groups inside of Templates, e.g. Flask
    template_group_path, templates = get_templates(template_groups) # The name of the folders inside of the Chosen TemplateGroup/Type (Default example: Flask)
    template_group_name = os.path.basename(template_group_path)
    template_index = query_manager(templates, "Choose a template from the list above.") # The index of what template you chose, so if it is the first one, it would be 0
    template_type = templates[template_index] # Gets the name of the Template

    source_folder = os.path.join(template_group_path, template_type) # Gets the folder of the chosen template

    settings_functions = SettingFunctions() # This gets the Functions that the TemplateOptions use, e.g. ChangePort which is used by all the Default Templates.

    shutil.copytree(source_folder, destination_folder) # Copies the chosen folder with the new name and the directory

    if not confirm(f"Would you like to Change some settings of {name}? (Y/N) "): # If you would like to continue with some settings
        color_print("Setup Complete!", "green")
        return 

    while True: # While the user has not exited or there was not a major error

        merged_options = resolve_options(template_options, template_group_name, template_type, global_options, TemplateGlobal_options)

        if not merged_options:
            error_print(f"No Options found for {template_type}, if this is a custom Template make sure to add a settings to TemplateSettings.json.")
            break
            
        options_keys = list(merged_options.keys()) # The name of each Option, e.g. "Change Port", "Exit"
        options_keys.append("Exit")

        index = query_manager(options_keys, "Choose what you want to edit.") # Gets the index of what option you want to do, e.g. Option 1 Chane Port the index would be 0
        option_key = options_keys[index]
        
        if option_key.strip() == "Exit":
            break

        function_name = merged_options[option_key] #  if option_key in merged_options else ""           # Gets the name of the function connected to the Option, e.g "Change Port" would get "ChangePort" function
        if not function_name:
            if option_key in shortcuts_options:
                function_name = shortcuts_options.get(option_key)

        execute_option(settings_functions, function_name, template_type, destination_folder)

if __name__ == "__main__":
    main()
