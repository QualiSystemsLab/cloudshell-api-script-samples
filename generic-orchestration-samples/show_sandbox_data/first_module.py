from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.sandbox_print_helpers import *


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

    warn_print(api, sandbox.id, "=== Current Sandbox Data ===")
    data = api.GetSandboxData(res_id)
    for data in data.SandboxDataKeyValues:
        outp = "sb_data_key: {}\n{}".format(data.Key, data.Value)
        sb_print(api, res_id, outp)
        sb_print(api, res_id, "=========================")
