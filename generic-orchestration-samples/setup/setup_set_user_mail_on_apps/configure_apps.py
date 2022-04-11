import json

from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.api.cloudshell_api import AppConfiguration, ConfigParam

TARGET_RESOURCE_BOOL_ATTRIBUTE = "Update Mail"
APP_CONFIG_PARAM = "USER_MAIL"


def configure_sandbox_owner_mail_on_app(sandbox, components=None):
    """
    get user email and run configure apps on apps matching boolean attribute True on resource
    :param Sandbox sandbox:
    :param components:
    :return:
    """
    api = sandbox.automation_api
    sb_id = sandbox.id
    logger = sandbox.logger
    sandbox_owner = sandbox.reservation_description.Owner
    owner_mail = api.GetUserDetails(sandbox_owner).Email
    if not owner_mail:
        raise ValueError("No email configured for user: {}".format(sandbox_owner))

    # find apps with target attribute
    all_resources = api.GetReservationDetails(reservationId=sb_id, disableCache=True).ReservationDescription.Resources
    target_resources = []
    for curr_resource in all_resources:
        details = api.GetResourceDetails(curr_resource.Name)
        attrs = details.ResourceAttributes
        attr_search = [x for x in attrs if x.Name == TARGET_RESOURCE_BOOL_ATTRIBUTE]
        if attr_search:
            attr_value = attr_search[0].Value
            if attr_value.lower() == "true":
                target_resources.append(curr_resource)

    if not target_resources:
        warn_msg = "No target resources found to set mail on"
        api.WriteMessageToReservationOutput(sb_id, warn_msg)
        logger.warn(warn_msg)

    updated_app_names = [x.Name for x in target_resources]
    all_other_apps = [x for x in all_resources if x.Name not in updated_app_names and x.CreatedInReservation]
    app_configurations = []
    for resource in target_resources:
        app_configurations.append(AppConfiguration(AppName=resource.Name,
                                                   ConfigParams=[ConfigParam(APP_CONFIG_PARAM, owner_mail)]))
    for resource in all_other_apps:
        app_configurations.append(AppConfiguration(AppName=resource.Name, ConfigParams=[]))

    config_msg = "Configuring following apps with sandbox owner email: {}\n{}".format(sandbox_owner,
                                                                                      json.dumps(updated_app_names, indent=4))
    logger.info(config_msg)
    api.WriteMessageToReservationOutput(sb_id, config_msg)
    api.ConfigureApps(reservationId=sb_id, appConfigurations=app_configurations, printOutput=True)
