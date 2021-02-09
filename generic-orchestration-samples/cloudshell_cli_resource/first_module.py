from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.sandbox_print_helpers import *
import helper_code.automation_api_helpers as api_help
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_help
import json
import cloudshell_cli_handler
import os

# command = os.environ['command']

# ========== Primary Function ==========
def first_module_flow(sandbox, components=None):
    """
    Functions passed into orchestration flow MUST have (sandbox, components) signature
    :param Sandbox sandbox:
    :param components
    :return:
    """
    api = sandbox.automation_api
    res_id = sandbox.id
    logger = sandbox.logger

    # Get resource Context snippet - relevant for resource scripts
    res_details = script_help.get_resource_context_details()
    sb_print(api, res_id, "resource name is: " + res_details.name)

    user, password = api_help.get_resource_credentials(api, res_details.name)
    host = res_details.address
    my_session = cloudshell_cli_handler.CreateSession(
        host=host,
        username=user,
        password=password,
        logger=logger
    )
    if not isinstance(command, list):
        commands = [command]
    else:
        commands = command
    outp = my_session.send_terminal_command(commands, password=password)
    logger.info(outp)
    return outp
