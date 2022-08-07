from cloudshell.api.cloudshell_api import SetConnectorRequest, ReservationDescriptionInfo, AppConfiguration, ConfigParam
from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.helpers.sandbox_reporter.reporter import SandboxReporter

#  These substrings must be in apps on canvas
LINUX_ES_SUBSTRING = "ansible es"
CLOUDSHELL_APP_SUBSTRING = "cloudshell"

LINUX_CLOUDSHELL_IP_PARAM = "CS_HOST"


def get_quali_server_resource(details: ReservationDescriptionInfo):
    quali_server_search = [x for x in details.Resources if CLOUDSHELL_APP_SUBSTRING in x.Name.lower()]
    if not quali_server_search:
        raise ValueError("Quali Server App not found on canvas")
    return quali_server_search[0]


def get_linux_es_app(details: ReservationDescriptionInfo):
    linux_es_search = [x for x in details.Resources if LINUX_ES_SUBSTRING in x.Name.lower()]
    if not linux_es_search:
        raise ValueError("Linux ES not found on canvas")
    return linux_es_search[0]


# ========== Primary Function ==========
def configure_linux_es(sandbox, components=None):
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
    details = api.GetReservationDetails(res_id, True).ReservationDescription
    linux_es = get_linux_es_app(details)
    quali_server = get_quali_server_resource(details)
    linux_params = [ConfigParam(LINUX_CLOUDSHELL_IP_PARAM, quali_server.FullAddress)]
    app_configs = [AppConfiguration(AppName=linux_es.Name, ConfigParams=linux_params)]
    try:
        api.ConfigureApps(reservationId=res_id, appConfigurations=app_configs, printOutput=False)
    except Exception as e:
        reporter.error(f"Issue configuring Linux ES. {type(e)}: {str(e)}")
        raise

    reporter.success("ES Registration Flow Done")
