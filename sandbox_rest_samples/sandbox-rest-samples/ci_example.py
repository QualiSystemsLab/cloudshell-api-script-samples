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

TARGET_BLUEPRINT = "<MY_BLUEPRINT_NAME>"
DEPLOYED_SANDBOX_NAME = "My Rest Api Blueprint"

api = SandboxRestApiSession(host=CS_SERVER, username=CS_USER, password=CS_PASSWORD, domain=CS_DOMAIN)
components_response = api.get_sandbox_components(sandbox_id)
print("===== GETTING COMPONENT DETAILS IN SANDBOX =====")
print(f"total components in sandbox: {len(components_response)}")
print(f"components response:\n{json.dumps(components_response, indent=4)}")

linux_server_search = [x for x in components_response if x["component_type"] == "Linux Server"]
if not linux_server_search:
    raise ValueError("linux server resource not found")

linux_server = linux_server_search[0]
linux_server_id = linux_server["id"]

print("===== RUNNING COMMAND TO LINUX SERVER =====")
params = [InputParam("command", "ifconfig")]
command_response = api.run_component_command(sandbox_id=sandbox_id,
                                             component_id=linux_server_id,
                                             command_name="send_custom_command",
                                             params=params)

execution_id = command_response["executionId"]
command_completed = False
output = None
while not command_completed:
    details = api.get_execution_details(execution_id)
    status = details["status"]
    if status.lower() in ["completed", "failed"]:
        command_completed = True
        output = details["output"]
    time.sleep(10)

if output:
    print(f"command output: {output}")

print("sandbox api commands finished")