from rich import print

def SuccessPrint(inputText):
    ColorPrint(inputText, "green")

def ErrorPrint(inputText):
    ColorPrint("Error: " + inputText, "red")

def ColorPrint(inputText, color):
    print(f"[{color}]{inputText}[/{color}]", end="\n")
