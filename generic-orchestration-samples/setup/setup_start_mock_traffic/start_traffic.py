from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.api.cloudshell_api import InputNameValue

TRAFFIC_CONTROLLER_MODEL = "Trafficshell"


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
    resources = res_details.Resources
    traffic_controller_search = [x for x in resources if x.ResourceModelName == TRAFFIC_CONTROLLER_MODEL]
    if not traffic_controller_search:
        raise ValueError(f"Traffic Controller Service '{TRAFFIC_CONTROLLER_MODEL}' not found on canvas")

    if len(traffic_controller_search) > 1:
        raise ValueError("Multiple traffic controllers found. Adjust script logic")

    traffic_controller = traffic_controller_search[0]

    api.WriteMessageToReservationOutput(reservationId=res_id, message=f"Starting traffic on {traffic_controller.Name}...")
    api.ExecuteCommand(reservationId=res_id,
                       targetName=traffic_controller.Name,
                       targetType="Resource",
                       commandName="start_traffic",
                       printOutput=True)

    api.WriteMessageToReservationOutput(reservationId=res_id, message="load config flow finished")

