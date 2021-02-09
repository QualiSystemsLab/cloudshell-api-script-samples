from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.thread_helpers import get_thread_results
from helper_code.custom_helpers import get_deployed_app_resources


def power_on_deployed_apps(sandbox, deployed_apps):
    # uses multi-threading
    def power_on_wrapper(sandbox, device):
        """
        :param Sandbox sandbox:
        :param TopologyReservedResourceInfo device:
        :return: ExecuteCommand response
        """
        return sandbox.automation_api.ExecuteResourceConnectedCommand(reservationId=sandbox.id,
                                                                      resourceFullPath=device.Name,
                                                                      commandName="PowerOn",
                                                                      commandTag="power",
                                                                      printOutput=True)

    threaded_power_off_apps = get_thread_results(sandbox=sandbox,
                                                 device_list=deployed_apps,
                                                 command_wrapper=power_on_wrapper)
    pass


def first_module_flow(sandbox, components=None):
    """
    Function passed to orchestration flow MUST have two parameters
    :param Sandbox sandbox:
    :param components
    :return:
    """
    deployed_apps = get_deployed_app_resources(sandbox)
    power_on_deployed_apps(sandbox, deployed_apps)
    pass



