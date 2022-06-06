from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.helpers.sandbox_reporter.reporter import SandboxReporter


PUBLIC_IP_ATTR = "Public IP"


def set_public_ip_flow(sandbox, components=None):
    """
    run all other playbooks on apps besides the router ones
    :param Sandbox sandbox:
    """
    api = sandbox.automation_api
    res_id = sandbox.id
    logger = sandbox.logger
    reporter = SandboxReporter(api, res_id, logger)
    resources = api.GetReservationDetails(res_id, True).ReservationDescription.Resources

    for resource in resources:
        res_details = api.GetResourceDetails(resource.Name)
        attrs = res_details.ResourceAttributes
        attrs_dict = {x.Name: x.Value for x in attrs}
        public_ip = attrs_dict.get(PUBLIC_IP_ATTR)
        if public_ip:
            reporter.warning(f"Updating address to public IP on {resource.Name}")
            api.UpdateResourceAddress(resourceFullPath=resource.Name, resourceAddress=public_ip)

    reporter.info("set public IP flow done", console_print=False)


