from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow


GLOBAL_INPUT_KEY = "My Global Input"


def hello_world_from_global_input(sandbox, components=None):
    """
    read global input and print out
    :param Sandbox sandbox:
    :param components:
    :return:
    """
    api = sandbox.automation_api
    sb_id = sandbox.id
    global_inputs_dict = sandbox.global_inputs
    my_global = global_inputs_dict.get(GLOBAL_INPUT_KEY)
    if not my_global:
        raise ValueError("Key of {} not found in sandbox Global inputs".format(GLOBAL_INPUT_KEY))
    msg = "User value for input '{}' is '{}'".format(GLOBAL_INPUT_KEY, my_global)
    api.WriteMessageToReservationOutput(reservationId=sb_id, message=msg)


sandbox = Sandbox()

DefaultSetupWorkflow().register(sandbox)
sandbox.workflow.add_to_preparation(hello_world_from_global_input)

sandbox.execute_setup()
