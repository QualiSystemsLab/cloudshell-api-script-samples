from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.sandbox_print_helpers import *
import helper_code.automation_api_helpers as api_help
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_help

JUNIPER_MODEL = "Juniper JunOS Switch 2G"


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
    resources = res_details.Resources
    juniper_resources = [resource for resource in resources
                         if resource.ResourceModelName == JUNIPER_MODEL]
    if not juniper_resources:
        raise Exception("No Juniper")

    juniper1 = juniper_resources[0]
    outp = api.ExecuteCommand(reservationId=res_id,
                              targetName=juniper1.Name,
                              targetType="Resource",
                              commandName="health_check",
                              printOutput=True).Output

    if "passed" in outp:
        pass
    elif "failed" in outp:
        raise Exception("Juniper Health Check Failed. Please check connectivity or VPN")

    pass
