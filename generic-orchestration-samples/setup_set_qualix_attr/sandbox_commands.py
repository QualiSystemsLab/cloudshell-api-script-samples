from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.sandbox_reporter import SandboxReporter

QUALIX_ADDRESS_ATTR = "QualiX_Address"
QUALIX_RESOURCE_MODEL = "QualiX Server"
REQUESTED_STATIC_IP_ATTR = "Requested Static IP"

SET_QUALIX_ADDRESS_COMMAND = "set qualix addresses"


class SandboxCommands(object):
    def __init__(self, reporter):
        """
        :param SandboxReporter reporter:
        """
        self.reporter = reporter

    def set_qualix_addresses(self, sandbox, components=None):
        """
        Functions passed into orchestration flow MUST have (sandbox, components) signature
        :param Sandbox sandbox:
        :param components
        :return:
        """
        api = sandbox.automation_api
        reporter = self.reporter
        all_resources = sandbox.reservation_description.Resources

        qualix_server_filter = [x for x in all_resources if x.ResourceModelName == QUALIX_RESOURCE_MODEL]
        if not qualix_server_filter:
            reporter.warn_out("No QualiX Model Resource found. Skipping '{}'".format(SET_QUALIX_ADDRESS_COMMAND))
            return

        if len(qualix_server_filter) > 1:
            err_msg = "More than one QualiX server on canvas. Script logic not supported"
            reporter.err_out(err_msg)
            raise Exception(err_msg)

        qualix_resource = qualix_server_filter[0]
        qualix_networks = qualix_resource.VmDetails.NetworkData
        mgmt_network_filter = [x for x in qualix_networks if not x.IsPrimary]
        if not mgmt_network_filter:
            reporter.warn_out("Management network on QualiX not found. Skipping '{}' action".format(SET_QUALIX_ADDRESS_COMMAND))
            return

        mgmt_ip = mgmt_network_filter[0].NetworkId

        all_other_apps = [x for x in all_resources if x.ResourceModelName != QUALIX_RESOURCE_MODEL]
        reporter.warn_out("Setting QualiX Address attribute to '{}'".format(mgmt_ip))
        for curr_app in all_other_apps:
            api.SetAttributeValue(resourceFullPath=curr_app.Name,
                                  attributeName=QUALIX_ADDRESS_ATTR,
                                  attributeValue=mgmt_ip)

    def set_requested_static_ip(self, sandbox, components=None):
        """
        Functions passed into orchestration flow MUST have (sandbox, components) signature
        :param Sandbox sandbox:
        :param components
        :return:
        """
        api = sandbox.automation_api
        reporter = self.reporter
        all_resources = sandbox.reservation_description.Resources

        for curr_resource in all_resources:
            app_details = api.GetResourceDetails(curr_resource.Name)
            attrs = app_details.ResourceAttributes
            attrs_dict = {attr.Name: attr.Value for attr in attrs}
            requested_static_ip = attrs_dict.get(REQUESTED_STATIC_IP_ATTR)
            if requested_static_ip:
                reporter.warn_out("Setting IP '{}' on resource '{}'".format(requested_static_ip, curr_resource.Name))
                api.UpdateResourceAddress(resourceFullPath=curr_resource.Name,
                                          resourceAddress=requested_static_ip)