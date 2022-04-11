# Dynamic Orchestration Template

A "one-size-fits-all" template for orchestration scripts.

How to use:
- Set your cloudshell credentials in dev_tools/crendentials.py
- In control_flow.py select your SCRIPT_TYPE [default, setup, teardown, resource, service].
- Attach to live sandbox for development by setting DEBUG_MODE to True.
- Run and Debug from main.py
- Includes a script to zip and upload in Cloudshell portal (load_to_cs.py).

If template is missing *credentials.py* file due to exclusion from Git, add the file to "dev_tools" folder.
Include the following python dictionary (adjust with your credentials):

```python

credentials = {
    "user": "admin",
    "password": "admin",
    "domain": "Global",
    "server": "localhost"
}

```




