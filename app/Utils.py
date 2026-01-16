#Utils.py, this is here because this is used by both app.py and Template_functions, so this reduces code reusability 

from rich import print

def success_print(inputText):
    color_print(inputText, "green")

def error_print(inputText):
    color_print("Error: " + inputText, "red")

def color_print(inputText, color):
    print(f"[{color}]{inputText}[/{color}]", end="\n")
