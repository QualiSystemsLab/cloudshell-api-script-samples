import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_help
from cloudshell.logging.qs_logger import get_qs_logger
from azure_routing_helper import set_virtual_appliance_routes
from cloudshell.helpers.sandbox_reporter.reporter import SandboxReporter


def set_firewall_routes_flow():
    # script helpers to pull in sandbox details, resource details, and api session
    api = script_help.get_api_session()
    sb_context = script_help.get_reservation_context_details()
    res_id = sb_context.id
    resource_details = script_help.get_resource_context_details()
    resource_name = resource_details.name
    resource_details = api.GetResourceDetails(resource_name)
    resource_model = resource_details.ResourceModelName
    logger = get_qs_logger(log_group=res_id,
                           log_category=resource_model,
                           log_file_prefix=resource_name)
    reporter = SandboxReporter(api, res_id, logger)

    # validate that resource is an app
    if not resource_details.VmDetails:
        exc_msg = f"{resource_name} is NOT an Azure deployed app resource, no cloud provider found."
        reporter.error(exc_msg)
        raise Exception(exc_msg)
    cloud_provider_resource_name = resource_details.VmDetails.CloudProviderFullName

    set_virtual_appliance_routes(va_resource_name=resource_name,
                                 clp_resource_name=cloud_provider_resource_name,
                                 api=api,
                                 res_id=res_id,
                                 reporter=reporter)

    # reporter.warning("power cycle virtual appliance")
