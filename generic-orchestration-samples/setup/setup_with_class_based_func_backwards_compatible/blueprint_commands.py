from extended_models import CustomSandbox
from cloudshell.workflow.orchestration.components import Components


class BlueprintCommands(object):
    def __init__(self, sandbox):
        """
        :param CustomSandbox sandbox:
        """
        self.sandbox = sandbox

    def command_one(self):
        api = self.sandbox.automation_api
        api.WriteMessageToReservationOutput(self.sandbox.id, "hello from bound method no param")


def command_with_sandbox_param(sandbox):
    """
    :param CustomSandbox sandbox:
    :return:
    """
    api = sandbox.automation_api
    api.WriteMessageToReservationOutput(sandbox.id, "hello from function with sandbox param only")


def command_with_sandbox_and_components_params(sandbox, components=None):
    """
    :param CustomSandbox sandbox:
    :param Components components:
    :return:
    """
    api = sandbox.automation_api
    api.WriteMessageToReservationOutput(sandbox.id, "hello from function with sandbox and component params")
