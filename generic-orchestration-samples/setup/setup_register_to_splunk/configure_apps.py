from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.api.cloudshell_api import AppConfiguration, ConfigParam

SERVER_IP_PARAM = "SERVER_IP"


def custom_configure_apps(sandbox, components=None):
    """
    :param Sandbox sandbox:
    :param components:
    :return:
    """
    api = sandbox.automation_api
    sb_id = sandbox.id
    logger = sandbox.logger
    resources = api.GetReservationDetails(sb_id, disableCache=True).ReservationDescription.Resources
    deployed_apps = [x for x in resources if x.VmDetails]
    if not deployed_apps:
        raise ValueError("No deployed apps found")
    clients = [x for x in deployed_apps if "splunk" not in x.Name.lower()]
    splunk_server_search = [x for x in deployed_apps if "splunk" in x.Name.lower()]
    if not splunk_server_search:
        raise ValueError("No splunk server found")
    if not clients:
        raise ValueError("No clients found to register to splunk")

    splunk_server = splunk_server_search[0]
    app_configs = []
    for client in clients:
        logger.info(f"updating dynamic splunk server IP on client script: {splunk_server.FullAddress}")
        params = [ConfigParam(SERVER_IP_PARAM, splunk_server.FullAddress)]
        config = AppConfiguration(AppName=client.Name, ConfigParams=params)
        app_configs.append(config)

    logger.info("starting configuration...")
    api.WriteMessageToReservationOutput(sb_id, "Starting registration to splunk")
    response = api.ConfigureApps(reservationId=sb_id, appConfigurations=app_configs, printOutput=True)
    failures = []
    for result in response.ResultItems:
        if result.Error:
            failures.append(result.AppName)
    if failures:
        raise Exception(f"Failed configurations: {failures}")
    msg = "Configuration Flow Done"
    logger.info(msg)
    api.WriteMessageToReservationOutput(sb_id, msg)

    api.WriteMessageToReservationOutput(sb_id, "Refreshing IP on all vms")
    for curr_app in deployed_apps:
        api.ExecuteResourceConnectedCommand(reservationId=sb_id,
                                            resourceFullPath=curr_app.Name,
                                            commandTag="remote_connectivity",
                                            commandName="remote_refresh_ip")
    api.WriteMessageToReservationOutput(sb_id, "Done refreshing IP")
