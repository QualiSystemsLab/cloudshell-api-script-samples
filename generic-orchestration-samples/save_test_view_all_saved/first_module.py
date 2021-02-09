from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.sandbox_print_helpers import *
import helper_code.automation_api_helpers as api_help
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_help


# ========== Primary Function ==========
def first_module_flow(sandbox):
    """
    Functions passed into orchestration flow MUST have (sandbox, components) signature
    :param Sandbox sandbox:
    :return:
    """
    api = sandbox.automation_api
    res_id = sandbox.id


    saved_sbs = api.GetSavedSandboxes().SavedSandboxes

    warn_print(api, sandbox.id, "=== current list of saved sandboxes ===")
    for sb in saved_sbs:
        sb_print(api, res_id, "Name: {}, ID: {}, BP origin: {}".format(sb.Name, sb.Id, sb.OriginatingBlueprintName))
