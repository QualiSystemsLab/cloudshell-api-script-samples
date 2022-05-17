from cloudshell.workflow.orchestration.sandbox import Sandbox

DUT_MODEL = "Putshell"


class HealtCheckException(Exception):
    pass


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
        raise Exception("No DUT resource found")

    dut1 = dut_resources[0]

    try:
        api.ExecuteCommand(reservationId=res_id,
                           targetName=dut1.Name,
                           targetType="Resource",
                           commandName="health_check",
                           printOutput=True)
    except Exception as e:
        err_msg = f"Issue caught during health check. {str(e)}"
        api.WriteMessageToReservationOutput(err_msg)
        raise HealtCheckException(err_msg)
