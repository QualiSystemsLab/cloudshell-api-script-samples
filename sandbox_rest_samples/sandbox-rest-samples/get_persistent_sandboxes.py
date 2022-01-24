import json

from cloudshell.sandbox_rest.sandbox_api import SandboxRestApiSession

# pull in api user credentials
CS_SERVER = "localhost"
CS_USER = "admin"
CS_PASSWORD = "admin"
CS_DOMAIN = "Global"

WHITELISTED_PERSISTENT_BP_IDS = []

api = SandboxRestApiSession(host=CS_SERVER, username=CS_USER, password=CS_PASSWORD, domain=CS_DOMAIN)
active_sandboxes = api.get_sandboxes()

illegal_persistent_sandboxes = []
for sandbox in active_sandboxes:
    sandbox_details = api.get_sandbox_details(sandbox["id"])
    if sandbox_details["blueprint_id"] in WHITELISTED_PERSISTENT_BP_IDS:
        continue

    if not sandbox_details["end_time"]:
        illegal_persistent_sandboxes.append(sandbox_details)

if not illegal_persistent_sandboxes:
    print("no unauthorized persistent sandboxes found")
else:
    print("Found unauthorized persistent sandboxes")
    print(json.dumps(illegal_persistent_sandboxes, indent=4))
