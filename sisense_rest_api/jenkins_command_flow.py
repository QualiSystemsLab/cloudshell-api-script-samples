"""
This flow:
1.Jenkins will start sandbox and return json string with sandbox id and state:
- ex: {"state":"Ready","name":"Jenkins Demo Sandbox","id":"4a51264a-e6bc-4fa9-9f4f-65f305f022af"}
2. start command on component, wait for execution to end, confirm execution status
"""

from credentials import credentials
from sandbox_polling_helpers import get_execution_data_upon_completion
from sisense_rest_build_elasticube import SandboxRest
import argparse

# GET SANDBOX ID FROM JENKINS
parser = argparse.ArgumentParser()
parser.add_argument("sandbox_id", help="sandbox id returned from jenkins")
args = parser.parse_args()
sandbox_id = args.sandbox_id

# BLUEPRINT SPECIFIC CONSTANTS
TARGET_COMPONENT_NAMES = ["mock_1", "mock_2"]
TARGET_COMPONENT_NAME = "mock_1"
FIRST_COMMAND_NAME = "health_check"
SECOND_COMMAND_NAME = "print_resource_details"

# instantiate rest session
sb_rest = SandboxRest(server=credentials["server"],
                      username=credentials["username"],
                      password=credentials["password"],
                      domain=credentials["domain"])


# HELPER METHODS
def get_target_component_data(target_component_name, sandbox_components_list):
    target_component_search = [component for component in sandbox_components_list if
                               component["name"] == target_component_name]
    if target_component_search:
        target_component = target_component_search[0]
        return target_component
    else:
        print("can't find target component in sandbox. Please check that your component exists")
        raise Exception("can't find target component")


def run_component_command(target_component, command_name):
    # Start command
    print("starting '{}' command on '{}' resource...".format(command_name, target_component["name"]))
    start_command_response = sb_rest.start_component_command(sandbox_id=sandbox_id,
                                                             component_id=target_component["id"],
                                                             command_name=command_name,
                                                             print_output=True)
    command_execution_id = start_command_response["executionId"]
    print("execution id of '{}' command: {}".format(command_name, command_execution_id))
    print("polling command '{}' execution completion state...".format(command_name))
    execution_data = get_execution_data_upon_completion(sandbox_rest=sb_rest,
                                                        command_execution_id=command_execution_id,
                                                        polling_frequency_in_seconds=10)
    execution_output = execution_data["output"]
    print("'{}' execution output: {}".format(command_name, execution_output))
    print("==========")
    return execution_output


def run_commands_on_component(target_component_name, sb_components):
    # find target component to run command on
    target_component = get_target_component_data(target_component_name, sb_components)
    # run both commands in series
    run_component_command(target_component, FIRST_COMMAND_NAME)
    run_component_command(target_component, SECOND_COMMAND_NAME)


# sandbox_data = sb_rest.get_sandbox_data(sandbox_id=sandbox_id)
# sandbox_components = sandbox_data["components"]
sandbox_components = sb_rest.get_sandbox_components(sandbox_id)

for component_name in TARGET_COMPONENT_NAMES:
    run_commands_on_component(target_component_name=component_name,
                              sb_components=sandbox_components)

