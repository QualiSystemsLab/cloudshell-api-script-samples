from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.sandbox_print_helpers import *
import helper_code.automation_api_helpers as api_help
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_help

TARGET_MODEL = "Putshell"

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
    resources = api.GetReservationDetails(res_id).ReservationDescription.Resources
    target_resources = [r for r in resources if r.ResourceModelName == TARGET_MODEL]
    if not target_resources:
        raise Exception("No resources of model {} found".format(TARGET_MODEL))

    for resource in target_resources:
        response = api.ExecuteCommand(reservationId=res_id,
                                      targetName=resource.Name,
                                      targetType="Resource",
                                      commandName="send_custom_cli_command",
                                      printOutput=True)


