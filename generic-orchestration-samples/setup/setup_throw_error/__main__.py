from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from time import sleep


DUT_MODEL = "Putshell"

sandbox = Sandbox()


def health_check_dut(sandbox, components=None):
    """
    :param Sandbox sandbox:
    :param components:
    :return:
    """
    sb_id = sandbox.id
    api = sandbox.automation_api
    resources = api.GetReservationDetails(sb_id, disableCache=True).ReservationDescription.Resources
    duts = [x for x in resources if x.ResourceModelName == DUT_MODEL]
    for dut in duts:
        api.WriteMessageToReservationOutput(sb_id, f"health checking resource {dut.Name}...")
        api.ExecuteCommand(reservationId=sb_id,
                           targetName=dut.Name,
                           targetType="Resource",
                           commandName="health_check",
                           printOutput=True)


def config_error_dut(sandbox, components=None):
    """

    :param Sandbox sandbox:
    :param components:
    :return:
    """
    sb_id = sandbox.id
    api = sandbox.automation_api
    resources = api.GetReservationDetails(sb_id, disableCache=True).ReservationDescription.Resources
    duts = [x for x in resources if x.ResourceModelName == DUT_MODEL]
    for dut in duts:
        api.WriteMessageToReservationOutput(sb_id, f"Starting config on {dut.Name}...")
        api.ExecuteCommand(reservationId=sb_id,
                           targetName=dut.Name,
                           targetType="Resource",
                           commandName="throw_error",
                           printOutput=True)


DefaultSetupWorkflow().register(sandbox)
sandbox.workflow.on_connectivity_ended(health_check_dut)
sandbox.workflow.add_to_configuration(config_error_dut)

sandbox.execute_setup()
