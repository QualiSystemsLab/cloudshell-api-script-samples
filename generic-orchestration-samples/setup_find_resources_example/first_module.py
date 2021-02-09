from cloudshell.workflow.orchestration.sandbox import Sandbox

TARGET_MODEL = "model name"


# ========== Primary Function ==========
def first_module_flow(sandbox, components=None):
    """
    Functions passed into orchestration flow MUST have (sandbox, components) signature
    :param Sandbox sandbox:
    :param components
    :return:
    """
    api = sandbox.automation_api
    res_id = sandbox.id
    reservation_details = api.GetReservationDetails(res_id).ReservationDescription
    resources = reservation_details.Resources

    # filter for target resources in sandbox
    target_reservation_resources = [r for r in resources if r.ResourceModelName == TARGET_MODEL]
    if not target_reservation_resources:
        raise Exception("resources with model '{}' not found".format(TARGET_MODEL))

    # see details of each resource including attributes
    for resource in target_reservation_resources:
        resource_details = api.GetResourceDetails(resourceFullPath=resource.Name)
        attrs = resource_details.ResourceAttributes

    # query cloudshell DB for resources NOT in sandbox
    all_target_resources = api.FindResources(resourceModel=TARGET_MODEL).Resources
    pass