# Orchestration Template

If credentials.py file is missing from directory, create the file and add the following dictionary.

```python

credentials = {
    "user": "admin",
    "password": "admin",
    "domain": "Global",
    "server": "localhost"
}

```

- 

Some Explanation of files and tools included in template:
- main.py - The entry point of the script that will be executed at runtime. Contains boilerplate for different script type flows. (default, setup, teardown)
- requirements.txt - The list of dependencies of the script. Downloaded by cloudshell into dedicated virtual environment at runtime.
                     cloudshell-orch-core is the default package needed for orchestration automation. 
- first_module.py - File with custom business logic of script. As many modules as needed can be created and imported into main.py
- DEBUG.py - this is the entry point of the script used during development / debug sessions
- DEBUG_GLOBALS.py - Simple booleans that can be used to add conditional print statements, mock conditions, etc. needed during development.
                     These booleans will be switched to False by update_script.py. 
- update_script.py - Used to update script on cloudshell server. Must attach new scripts manually the first time. 
                     Run this script for subsequent updates.
- credentials.py - cloudshell user credentials used for attaching to debug sessions and updating script on server.
- .gitignore - Should you opt to check script into source control, add credentials.py and any other files you wish to exclude.
- helper_code - api helper functions and additonal modules are put in here to prevent clutter of main directory.                        
                   



