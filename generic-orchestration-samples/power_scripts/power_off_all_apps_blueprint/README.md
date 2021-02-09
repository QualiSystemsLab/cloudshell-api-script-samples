# Dynamic Orchestration Template

A "one-size-fits-all" template for orchestration scripts.

To set correct script flow:
- In __main__.py set SCRIPT_FLOW variable [default, setup, teardown].

To develop against live sandbox:
- Set your cloudshell credentials in credentials.py
- Set LIVE_SANDBOX_ID in DEBUG.py (can be found at end of URL of sandbox)
- Add service or resource name string (if writing a resource script)
- Run from DEBUG.py

To update script to cloudshell:
- Verify that credentials.py are set correctly.
- Run update_script.py
- NOTE: Credentials automatically replaced with placeholders in zip package when running update_script.py
- To exclude from version control be sure to add credentials.py to .gitignore

If credentials.py file is missing, create the file and add the following dictionary.

```python

credentials = {
    "user": "admin",
    "password": "admin",
    "domain": "Global",
    "server": "localhost"
}

```




