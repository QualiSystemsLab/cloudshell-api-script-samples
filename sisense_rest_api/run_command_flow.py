"""
This flow:
1.start sandbox, wait for setup to finish
2. start command on component, wait for execution to end, confirm execution status
3. end sandbox, poll for "Ended" status
"""

from credentials import credentials
from sandbox_polling_helpers import poll_sandbox_state, get_execution_data_upon_completion
from sisense_rest_build_elasticube import SandboxRest

# Enter blueprint name or blueprint ID (found in url of blueprint)
BLUEPRINT_ID = "befdaff4-d56d-489e-bec5-f889a9d26e61"
TARGET_COMPONENT_NAME = "dummy_put1"
TARGET_COMPONENT_COMMAND_NAME = "print_resource_details_with_timeout"

# instantiate session
sb_rest = SandboxRest(server=credentials["server"],
                      username=credentials["username"],
                      password=credentials["password"],
                      domain=credentials["domain"])

print("starting sandbox...")
sandbox_response = sb_rest.start_blueprint(blueprint_id=BLUEPRINT_ID, sandbox_name="Sandbox API Demo Sandbox")
sandbox_id = sandbox_response["id"]
sandbox_components_list = sandbox_response["components"]

# find target component to run command on
target_component_search = [component for component in sandbox_components_list if component["name"] == TARGET_COMPONENT_NAME]
if target_component_search:
    target_component = target_component_search[0]
else:
    print("can't find target component in sandbox. Please check that your component exists")
    raise Exception("can't find target component")

# wait for sandbox to start before triggering command
print("polling setup...")
poll_sandbox_state(sb_rest, sandbox_id)

# Start command
print("starting command on resource...")
start_command_response = sb_rest.start_component_command(sandbox_id=sandbox_id,
                                                         component_id=target_component["id"],
                                                         command_name=TARGET_COMPONENT_COMMAND_NAME)

command_execution_id = start_command_response["executionId"]
print("execution id of command: " + command_execution_id)

print("polling command execution completion state...")
execution_data = get_execution_data_upon_completion(sb_rest, command_execution_id)
execution_output = execution_data["output"]
print("execution output: " + execution_output)

print("stopping sandbox...")
sb_rest.stop_sandbox(sandbox_id)

print("polling sandbox for completion...")
poll_sandbox_state(sandbox_rest=sb_rest, reservation_id=sandbox_id)

