"""
Module for storing utility functions to be used across dev_tools files
"""
from cloudshell.api.common_cloudshell_api import CloudShellAPIError


def error_red(err_str):
    """
    for wrapping print statements in red to highlight errors
    :param err_str:
    :return:
    """
    CRED = '\033[91m'
    CEND = '\033[0m'
    return CRED + err_str + CEND


def attach_to_cs_wrapper(live_sandbox_id, resource_name=None, service_name=None):
    from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
    from credentials import credentials
    try:
        attach_to_cloudshell_as(user=credentials['user'],
                                password=credentials['password'],
                                domain=credentials['domain'],
                                reservation_id=live_sandbox_id,
                                server_address=credentials['server'],
                                resource_name=resource_name,
                                service_name=service_name)
    except CloudShellAPIError as e:
        print(error_red("error attaching to live sandbox:\n" + str(e)) +
              "\nTry checking user credentials, LIVE_SANDBOX_ID, TARGET_RESOURCE_NAME Spelling in control_flow.py")
        exit(1)
    except AttributeError as e:
        print(error_red("error attaching to live sandbox:\n" + str(e)) +
              "\nCheck spelling of TARGET_SERVICE_NAME set in control_flow.py")
        exit(1)


def get_sandbox_wrapper():
    from cloudshell.workflow.orchestration.sandbox import Sandbox
    try:
        sandbox = Sandbox()
    except KeyError as e:
        print(error_red('KeyError: ' + str(e)) + '\n' +
              'Be sure "attach_to_cloudshell_as" is executed while developing.\n'
              'Set DEBUG_MODE = True in control_flow.py.')
        exit(1)
    else:
        return sandbox


def get_res_details_wrapper():
    import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_help
    try:
        res_details = script_help.get_resource_context_details()
    except KeyError as e:
        print(error_red('KeyError: ' + str(e)) + '\n' +
              'Can not find the target Resource.\n'
              'Check TARGET_RESOURCE_NAME in control_flow.py.')
        exit(1)
    else:
        return res_details


