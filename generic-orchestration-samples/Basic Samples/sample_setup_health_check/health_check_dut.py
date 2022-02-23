from cloudshell.workflow.orchestration.sandbox import Sandbox


TARGET_MODEL = "Putshell"


def run_health_check(sandbox, components=None):
    """

    :param Sandbox sandbox:
    :param components:
    :return:
    """
    api = sandbox.automation_api
    sb_id = sandbox.id
    logger = sandbox.logger

    sandbox_details = api.GetReservationDetails(reservationId=sb_id, disableCache=True).ReservationDescription
    resources = sandbox_details.Resources
    dut_resource_search = [x for x in resources if x.ResourceModelName == TARGET_MODEL]
    if not dut_resource_search:
        raise ValueError(f"Could not find resource of model {TARGET_MODEL} in sandbox")

    for resource in dut_resource_search:
        api.WriteMessageToReservationOutput(sb_id, f"starting health check for {resource.Name}")
        api.ExecuteCommand(reservationId=sb_id,
                           targetName=resource.Name,
                           targetType="Resource",
                           commandName="health_check",
                           printOutput=True)

    done_message = "health checking done"
    api.WriteMessageToReservationOutput(sb_id, done_message)
    logger.info(done_message)


