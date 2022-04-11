from cloudshell.workflow.orchestration.sandbox import Sandbox

DUT_MODEL = "Putshell"


# ========== Primary Function ==========
def run_dut_health_check(sandbox, components=None):
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
    dut_resources = [resource for resource in resources
                     if resource.ResourceModelName == DUT_MODEL]
    if not dut_resources:
        raise Exception("No Juniper")

    dut1 = dut_resources[0]

    api.ExecuteCommand(reservationId=res_id,
                       targetName=dut1.Name,
                       targetType="Resource",
                       commandName="health_check",
                       printOutput=True)