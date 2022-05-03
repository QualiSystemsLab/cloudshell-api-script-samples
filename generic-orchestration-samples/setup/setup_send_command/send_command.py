from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.api.cloudshell_api import InputNameValue


LINUX_MODEL = "Linux Server"
COMMAND_STRING = "/root/hello_world.sh"


# ========== Primary Function ==========
def send_command(sandbox, components=None):
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
    logger = sandbox.logger
    logger.info("send command flow starting...")
    linux_resources = [resource for resource in resources
                       if resource.ResourceModelName == LINUX_MODEL]
    if not linux_resources:
        raise Exception("No Linux Server found")

    linux_resource = linux_resources[0]

    command_inputs = [InputNameValue("command", COMMAND_STRING)]
    output = api.ExecuteCommand(reservationId=res_id,
                                targetName=linux_resource.Name,
                                targetType="Resource",
                                commandName="send_custom_command",
                                commandInputs=command_inputs,
                                printOutput=True).Output

    # validate output
    if "hello world" not in output.lower():
        raise Exception(f"Command Validation failed. 'hello world' not found.\nOutput received: {output}")
