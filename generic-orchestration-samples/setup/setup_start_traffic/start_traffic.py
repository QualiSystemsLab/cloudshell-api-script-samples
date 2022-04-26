import os

from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.api.cloudshell_api import InputNameValue

TRAFFIC_CONTROLLER_MODEL = "BreakingPoint Controller 2G"
TRAFFIC_CONFIG_PATH_INPUT = "Traffic Config Path"


def start_traffic_flow(sandbox, components=None):
    """
    Functions passed into orchestration flow MUST have (sandbox, components) signature
    :param Sandbox sandbox:
    :param components
    :return:
    """
    api = sandbox.automation_api
    res_id = sandbox.id
    res_details = api.GetReservationDetails(res_id).ReservationDescription
    services = res_details.Services
    traffic_controller_search = [x for x in services if x.ServiceName == TRAFFIC_CONTROLLER_MODEL]
    if not traffic_controller_search:
        raise ValueError(f"Traffic Controller Service '{TRAFFIC_CONTROLLER_MODEL}' not found on canvas")

    if len(traffic_controller_search) > 1:
        raise ValueError("Multiple traffic controllers found. Adjust script logic")

    # validate global input
    global_inputs = sandbox.global_inputs
    traffic_config_path = global_inputs.get(TRAFFIC_CONFIG_PATH_INPUT)
    if not traffic_config_path:
        raise ValueError(f"No sandbox input found for: '{TRAFFIC_CONFIG_PATH_INPUT}'")

    traffic_controller = traffic_controller_search[0]

    api.WriteMessageToReservationOutput(reservationId=res_id, message=f"Loading traffic config '{traffic_config_path}'...")
    command_inputs = [InputNameValue("config_file_location", traffic_config_path)]
    api.ExecuteCommand(reservationId=res_id,
                       targetName=traffic_controller.Alias,
                       targetType="Service",
                       commandName="load_config",
                       commandInputs=command_inputs,
                       printOutput=True)

    api.WriteMessageToReservationOutput(reservationId=res_id, message="load config flow finished")

