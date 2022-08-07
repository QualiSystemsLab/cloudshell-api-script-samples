from cloudshell.api.cloudshell_api import SetConnectorRequest, ReservationDescriptionInfo
from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.helpers.sandbox_reporter.reporter import SandboxReporter

#  These substrings must be in apps on canvas
LINUX_ES_SUBSTRING = "ansible es"
CLOUDSHELL_APP_SUBSTRING = "cloudshell"

DEFAULT_DEPLOYMENT_PATH = "vCenter 2G VCSA - vCenter VM From Linked Clone 2G"
CLOUDSHELL_VERSION_INPUT = "Cloudshell Version"

CLOUDSHELL_LATEST_VERSION = "2022.1"
app_map = {
    "2022.1": "CloudShell 2022.1 GA",
    "2021.2": "CloudShell 2021.2 GA Patch 3",
    "2020.2": "CloudShell 2020.2 GA"
}


def get_quali_server_app(details: ReservationDescriptionInfo):
    quali_server_app_search = [x for x in details.Apps if CLOUDSHELL_APP_SUBSTRING in x.Name.lower()]
    if not quali_server_app_search:
        raise ValueError("Quali Server App not found on canvas")
    return quali_server_app_search[0]


def get_linux_es_app(details: ReservationDescriptionInfo):
    linux_es_search = [x for x in details.Apps if LINUX_ES_SUBSTRING in x.Name.lower()]
    if not linux_es_search:
        raise ValueError("Linux ES App not found on canvas")
    return linux_es_search[0]


# ========== Primary Function ==========
def replace_quali_server_app(sandbox, components=None):
    """
    Functions passed into orchestration flow MUST have (sandbox, components) signature
    :param Sandbox sandbox:
    :param components
    :return:
    """
    api = sandbox.automation_api
    res_id = sandbox.id
    logger = sandbox.logger
    reporter = SandboxReporter(api, res_id, logger)
    res_inputs = sandbox.global_inputs
    cs_version = res_inputs.get(CLOUDSHELL_VERSION_INPUT, "2022.1")
    if cs_version == CLOUDSHELL_LATEST_VERSION:
        return

    if cs_version not in app_map:
        supported_versions = app_map.keys()
        raise ValueError(f"Cloudshell Version {cs_version} not supported by setup. Supported: {supported_versions}")

    details = api.GetReservationDetails(res_id, True).ReservationDescription
    quali_server_app = get_quali_server_app(details)

    positions = api.GetReservationServicesPositions(res_id).ResourceDiagramLayouts
    quali_server_pos = [x for x in positions if quali_server_app.Name in x.ResourceName][0]

    reporter.warning(f"Switching out Quali Server for version: {cs_version}")
    api.RemoveAppFromReservation(reservationId=res_id, appName=quali_server_app.Name)
    api.AddAppToReservation(reservationId=res_id,
                            appName=app_map[cs_version],
                            deploymentPath=DEFAULT_DEPLOYMENT_PATH,
                            positionX=quali_server_pos.X + 500,
                            positionY=quali_server_pos.Y)



