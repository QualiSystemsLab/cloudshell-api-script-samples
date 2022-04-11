from extended_models import CustomSandbox


class BlueprintCommands(object):
    def __init__(self, sandbox):
        """
        :param CustomSandbox sandbox:
        """
        self.sandbox = sandbox

    def command_one(self):
        api = self.sandbox.automation_api
        api.WriteMessageToReservationOutput(self.sandbox.id, "hello from command one")

    def command_two(self):
        api = self.sandbox.automation_api
        api.WriteMessageToReservationOutput(self.sandbox.id, "hello from command two")