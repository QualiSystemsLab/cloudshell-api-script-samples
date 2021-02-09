from helper_code.sandbox_print_helpers import *
import helper_code.automation_api_helpers as api_help
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_help
import os
from DEBUG_GLOBALS import DEBUG_MODE
from cloudshell_cli_handler import CreateSession


# ========== Primary Function ==========
def send_cli_command_flow():
    """
    Functions passed into orchestration flow MUST have (sandbox, components) signature
    :param Sandbox sandbox:
    :param componentssc
    :return:
    """
    # script helpers to pull in sandbox details, resource details, and api session
    sb_context = script_help.get_reservation_context_details()
    resource_details = script_help.get_resource_context_details()
    api = script_help.get_api_session()

    res_id = sb_context.id
    host_ip = resource_details.address
    resource_name = resource_details.name
    attributes = resource_details.attributes
    user = api_help.get_resource_attr_val(api, resource_name, "User")
    encrypted_password = api_help.get_resource_attr_val(api, resource_name, "Password")
    decrypted_pass = api.DecryptPassword(encryptedString=encrypted_password).Value

    # Instantiate CLI
    cli = CreateSession(host_ip, user, decrypted_pass)
    sample_commands = ['hostname -I', "ifconfig"]
    outp = cli.send_commands_list(sample_commands)
    sb_print(api, res_id, outp)
    print("=== Command Successful ===")


