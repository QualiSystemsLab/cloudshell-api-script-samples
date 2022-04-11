from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.sandbox_print_helpers import *
import helper_code.automation_api_helpers as api_help
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_help


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
    warn_print(api, sandbox.id, "=== Hello from sandbox! ===")

    resources = api_help.get_reservation_resources(api, res_id)
    resource_count = len(resources)
    sb_print(api, res_id, "resource count in sandbox: " + str(resource_count))

    """
    # Get resource Context snippet - relevant for resource scripts
    res_details = script_help.get_resource_context_details()
    sb_print(api, res_id, "resource name is: " + res_details.name)
    """
