import json
import sys
import time

from cloudshell.sandbox_rest.sandbox_api import SandboxRestApiSession, InputParam

if len(sys.argv) < 2:
    raise ValueError("Sandbox Id not passed")

# sandbox ID is injected into script via command line argument
sandbox_id = sys.argv[1]

# pull in api user credentials
CS_SERVER = "localhost"
CS_USER = "admin"
CS_PASSWORD = "admin"
CS_DOMAIN = "Global"


api = SandboxRestApiSession(host=CS_SERVER, username=CS_USER, password=CS_PASSWORD, domain=CS_DOMAIN)
components_response = api.get_sandbox_components(sandbox_id)
print("===== GETTING COMPONENT DETAILS IN SANDBOX =====")
print(f"total components in sandbox: {len(components_response)}")
print(f"components response:\n{json.dumps(components_response, indent=4)}")

print(f"starting test on sandbox {sandbox_id}...")
time.sleep(30)
print("jenkins test done")