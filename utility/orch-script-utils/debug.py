"""
Example how to use "attach_to_cloudshell" helper
Take care not to commit cloudshell credentials to source control
"""
from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as


def custom_flow(sandbox, components=None):
    """

    :param Sandbox sandbox:
    :param components:
    :return:
    """
    sandbox.automation_api.WriteMessageToReservationOutput(sandbox.id, "hello from debug")


if __name__ == "__main__":
    LIVE_SANDBOX_ID = "bda46630-f777-401c-a27e-c055f6e6732b"
    attach_to_cloudshell_as(server_address="localhost",
                            user="admin",
                            password="admin",
                            domain="Global",
                            reservation_id=LIVE_SANDBOX_ID)

    sandbox = Sandbox()
    custom_flow(sandbox)
