from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.sandbox_print_helpers import *
from cloudshell.api.cloudshell_api import SandboxDataKeyValue
import os

INPUT_COMMAND_PARAMETER_1 = 'sb_data_key'
INPUT_COMMAND_PARAMETER_2 = 'sb_data_value'


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

    sb_data_key = os.environ[INPUT_COMMAND_PARAMETER_1]
    sb_data_value = os.environ[INPUT_COMMAND_PARAMETER_2]

    warn_print(api, sandbox.id, "=== Setting Sandbox Data Key ===")
    sb_print(api, res_id, "{}: {}".format(sb_data_key, sb_data_value))

    data1 = SandboxDataKeyValue(sb_data_key, sb_data_value)
    all_data = [data1]
    api.SetSandboxData(res_id, all_data)

