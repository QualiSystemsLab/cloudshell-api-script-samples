from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.SandboxReporter import *
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

    # FIND RESOURCES
    res_details = api.GetReservationDetails(reservationId=res_id).ReservationDescription
    resources = res_details.Resources
    put_resources = [r for r in resources if r.ResourceModelName == "Putshell"]
    if not put_resources:
        raise Exception("No Putshell resources in blueprint")

    # TRIGGER ACTIONS
    for resource in put_resources:
        sb_print(api, res_id, "Running Commands synchronously (Blocking)")
        response = api.ExecuteCommand(reservationId=res_id,
                                      targetName=resource.Name,
                                      targetType="Resource",
                                      commandName="health_check")

    pass
