from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.sandbox_print_helpers import *
import helper_code.automation_api_helpers as api_help
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_help
import time


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
    # Get resource Context snippet - relevant for resource scripts
    res_details = script_help.get_resource_context_details()
    sb_print(api, res_id, "resource name is: " + res_details.name)
    sb_print(api, res_id, "resource ip is: " + res_details.address)
    raise Exception("failed test")
