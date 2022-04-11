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

    res_details = api.GetReservationDetails(res_id).ReservationDescription
    blueprint_name = res_details.Topologies[0]

    warn_print(api, res_id, "activating topology, forwarding blueprint attributes")
    api.ActivateTopology(res_id, topologyFullPath=blueprint_name)
    pass
