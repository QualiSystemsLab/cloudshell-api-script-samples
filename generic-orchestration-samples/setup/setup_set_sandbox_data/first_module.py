from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.api.cloudshell_api import SandboxDataKeyValue
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

    data1 = SandboxDataKeyValue('Key1', 'Value1')
    data2 = SandboxDataKeyValue('Key2', 'Value2')

    all_data = [data1, data2]

    api.SetSandboxData(res_id, all_data)

    warn_print(api, sandbox.id, "=== Setting Sandbox Data! ===")
    sb_print(api, res_id, "Key1: Value1")
    sb_print(api, res_id, "Key2: Value2")


