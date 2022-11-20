from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.helpers.sandbox_reporter.reporter import SandboxReporter


def validate_cluster_flow(sandbox, components=None):
    """
    Workflow functions must have (sandbox, components) signature
    :param Sandbox sandbox:
    """
    api = sandbox.automation_api
    sb_id = sandbox.id
    logger = sandbox.logger
    reporter = SandboxReporter(api, sb_id, logger)  # logs to file and print to sandbox console

    reporter.warning("Validating Vcenter Cluster...")

    sb_details = api.GetReservationDetails(reservationId=sb_id, disableCache=True).ReservationDescription
    apps = sb_details.Apps
    default_deployment = [x for x in apps[0].DeploymentPaths if x.IsDefault][0]
    cloud_provider = default_deployment.DeploymentService.CloudProvider
    api.ExecuteCommand()
    reporter.info(f"Resource count in sandbox: {len(resources)}")

