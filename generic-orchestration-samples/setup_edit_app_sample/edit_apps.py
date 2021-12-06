from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.api.cloudshell_api import CloudShellAPISession, ApiEditAppRequest, AppDetails, DefaultDeployment, Deployment, \
    NameValuePair


def edit_target_app_in_sandbox(app_name, new_app_name, api, sb_id, target_deployment_attrs):
    """
    the target deployment attrs ignores namespacing and case sensitivity.
    This will work for the hdd and cpu attrs - [("hdd", "3"), ("cpu", "5")]
    :param str app_name:
    :param str new_app_name:
    :param CloudShellAPISession api:
    :param str sb_id:
    :param list target_deployment_attrs: example [("hdd", "3"), ("cpu", "5")]
    :return:
    """
    target_deployment_attrs = target_deployment_attrs or []
    # find target app to modify
    apps = api.GetReservationDetails(sb_id, disableCache=True).ReservationDescription.Apps
    if not apps:
        return
    target_app_search = [app for app in apps if app.Name == app_name]
    if not target_app_search:
        return
    target_app = target_app_search[0]

    # copy over logical resource attributes
    new_resource_attrs = []
    for curr_attr in target_app.LogicalResource.Attributes:
        new_resource_attrs.append(NameValuePair(curr_attr.Name, curr_attr.Value))

    default_deployment = [x for x in target_app.DeploymentPaths if x.IsDefault][0]

    # copy over all deployment attributes, modify target attributes
    new_deployment_attrs_map = {}
    for curr_attr in default_deployment.DeploymentService.Attributes:
        for update_attr_name, update_attr_value in target_deployment_attrs:
            if curr_attr.Name.lower().endswith(update_attr_name):
                new_deployment_attrs_map[curr_attr.Name] = update_attr_value
                break

        if curr_attr.Name not in new_deployment_attrs_map:
            new_deployment_attrs_map[curr_attr.Name] = curr_attr.Value

    # build out app edit request
    new_deployment_attrs_list = [NameValuePair(x[0], x[1]) for x in new_deployment_attrs_map.items()]
    new_deployment = Deployment(new_deployment_attrs_list)
    app_details = AppDetails(ModelName=target_app.LogicalResource.Model, Attributes=new_resource_attrs,
                             Driver=target_app.LogicalResource.Driver)
    new_default_deployment = DefaultDeployment(Name=default_deployment.Name, Deployment=new_deployment)
    app_edit_requests = [ApiEditAppRequest(Name=app_name,
                                           NewName=new_app_name,
                                           Description="",
                                           AppDetails=app_details,
                                           DefaultDeployment=new_default_deployment)]
    api.EditAppsInReservation(reservationId=sb_id, editAppsRequests=app_edit_requests)


def edit_apps_in_sandbox(sandbox, components):
    """

    :param Sandbox sandbox:
    :param components:
    :return:
    """
    api = sandbox.automation_api
    sb_id = sandbox.id
    APP_NAME = "TEST"
    NEW_NAME = "NATTI"
    target_deployment_attrs = [("hdd", "3"), ("cpu", "5")]

    edit_target_app_in_sandbox(app_name=APP_NAME,
                               new_app_name=NEW_NAME,
                               api=api,
                               sb_id=sb_id,
                               target_deployment_attrs=target_deployment_attrs)
