# ProjGen

`ProjGen` is a command-line tool for quickly scaffolding new projects. It provides an interactive interface to choose from a variety of pre-built templates, from a minimal single-file app to more complex structures with databases, blueprints, and Jinja templates. It's designed to be easily extensible, allowing you to add your own custom project templates.

## Features

- **Interactive CLI:** An easy-to-use command-line interface guides you through project setup.
- **Variety of Templates:** Start your project with one of the included templates:
    - **Basic:** A minimal, single-file Flask application.
    - **BasicDb:** An application with SQLAlchemy, Flask-Migrate, and a basic model structure.
    - **BasicTemplate:** An application demonstrating the use of Jinja2 templates.
    - **BlueprintDb:** An application structured using Flask Blueprints.
- **Post-Setup Configuration:** Modify common settings, like the application port, after the project has been created.
- **Extensible:** Easily add your own templates and custom configuration options.

## Installation

You can install `ProjGen` by cloning this repository and running the appropriate installation script. This will build the package and install the `ProjGen` command-line tool using `pipx` for isolated installation.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/FazpyDev/ProjGen.git
    cd ProjGen
    ```

2.  **Run the installation script:**

    **For Linux/macOS:**
    ```bash
    ./install.sh
    ```

    **For Windows:**
    ```batch
    .\install.bat
    ```

    The script will install the necessary dependencies, build the package, and install the `projgen` command.

## Usage

Once installed, you can create a new project by running the `projgen` command in your terminal.
OR you can create a new project without changing any settings of it quickly by running: 

```bash
projgen name templategroup templatename 
```

`name` is what you want to call the project, so the folders name, `templategroup` is what group you are copying,
like Flask, and `templatename` is what template you are copying.

But if you would like a more user friendly way and/or to change some of the settings, use this:

```bash
projgen
```

The tool will then guide you through the following steps:
1.  **Enter a Project Name:** This will be the name of your new project directory.
2.  **Choose a Template Group:** Select the category of template you want to use.
3.  **Choose a Template:** Select a specific template from the chosen group.
4.  **Configure Settings (Optional):** After the project is created, you'll have the option to modify settings, such as changing the default port.

## Extending with Custom Templates

One of the core features of `ProjGen` is its extensibility. You can add your own templates and associated configuration options.

### 1. Add Your Template Files

1.  Navigate to the `app/templates/` directory within the `ProjGen` source code.
2.  Create a new directory for your template group (e.g., `MyTemplates`).
3.  Inside your new group directory, create another directory for your specific template (e.g., `MyAwesomeApp`).
4.  Place all the files and folders for your project boilerplate inside the `MyAwesomeApp` directory.

The final structure will look like this:
```
app/
└── templates/
    └── MyTemplates/
        └── MyAwesomeApp/
            └── ... your other files
```

### 2. Add Custom Configuration Options

To add configurable settings for your template (like changing a port, an API key, etc.):

1.  **Define the option in `app/TemplateOptions.json`**:
    Open the `app/TemplateOptions.json` file. To add an option that only applies to your specific template, add an entry like this:

    ```json
    {
        "MyAwesomeApp": {
           "Option display name": "functionName"
        }
    }
    ```
    - `"MyAwesomeApp"`: Must match your template's folder name.
    - `"Option display name"`: The text that will be shown to the user in the CLI.
    - `"functionName"`: The name of the Python function that will execute the configuration logic.

2.  **Create the function in `app/template_Functions.py`**:
    Open `app/template_Functions.py` and add a new method to the `SettingFunctionsClass` with the `functionName` you specified. The method will receive the `template_type` and the `destination_folder` path as arguments.

    ```python
    # In app/template_Functions.py

    class SettingFunctionsClass():
        # ... other functions

        def functionName(self, filetype, destination_folder):
            # Your logic here.
            # For example, ask the user for input and modify a file.
            print(f"Configuring {filetype} in {destination_folder}...")
            # ...

## Template Options Features

### 1.Shortcuts

```json
{
    "Shortcuts": { 
        "Change Port": "change_port"
    }

    "MyAwesomeApp": {
        "Change Port": ""
    }

}
```
    
This is a global Shortcuts which means it is used everywhere, however if you do have a non global Shortcut it will be used instead
What it does is make it so you can put a function name once and use it wherever you want, this is so if you rename a function it wont be hard to change it up
You can also have shortcuts designed only for specific templateGroups, which use the syntax ```"Group-Shortcuts"```, for example:

```json
{
    "MyTemplates-Shortcuts": {
        "Change Port": "change_port"
    }

    "MyAwesomeApp": {
        "Change Port": ""
    }
```

If TemplateName is inside of the Template Group Flask, it will use the change_port function for the option "Change Port"
This is how the file structure should look like for this:
```
app/
└── templates/
    └── MyTemplates/
        └── MyAwesomeApp/
            └── ... your other files
```

### 2. Global

Global is a way to add options to every template, for example:

```json
{
    "Global": {
        "Change Port": "change_port"
    }
```

This will add the Change Port option linked to change_port function to EVERY template, even outside of Flask, which obviously probably wont work if your template is something outside of Flask, which is why you can add custom Globals
These custom Globals override the main global, so it will not take the options from it, for example:

```json
{
    "Global": {
        "Change Port": "change_port"
    }

    "MyTemplates-Global": {
        "Option": "NonExistantFunc"
    }
```

Inside every Template of MyTemplates it will only have the option "Option", I might add a way to choose to use both, but that will be later and probably wont happen unless people actually use this.

This is how the file structure should look like for this:
```
app/
└── templates/
    └── MyTemplates/
        └── MyAwesomeApp/
            └── ... your other files
```



