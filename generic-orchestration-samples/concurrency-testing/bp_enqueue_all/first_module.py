from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.sandbox_print_helpers import *
import helper_code.automation_api_helpers as api_help


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

    resources = api_help.get_reservation_resources(api, res_id)
    putshell_resources = [resource for resource in resources if resource.ResourceModelName == 'Putshell']
    for resource in putshell_resources:
        api.EnqueueCommand(reservationId=res_id,
                           targetName=resource.Name,
                           targetType="Resource",
                           commandName="resource_timed_sleep",
                           printOutput=True)
    pass