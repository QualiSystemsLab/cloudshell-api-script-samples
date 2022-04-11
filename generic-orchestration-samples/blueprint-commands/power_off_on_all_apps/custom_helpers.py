from cloudshell.workflow.orchestration.sandbox import Sandbox


def sb_print(sandbox, message):
    """
    convenience printing method for printing to reservation output
    :param Sandbox sandbox:
    :param str message:
    :return:
    """
    sandbox.automation_api.WriteMessageToReservationOutput(sandbox.id, message)


def get_reservation_resources(sandbox):
    """
    :param Sandbox sandbox:
    :return:
    """
    reservation_details = sandbox.automation_api.GetReservationDetails(reservationId=sandbox.id)
    resources = reservation_details.ReservationDescription.TopologiesReservedResources
    return resources


def get_reservation_resources_by_family(sandbox, family_name):
    """
    :param Sandbox sandbox:
    :param str family_name:
    :return:
    """
    resources = get_reservation_resources(sandbox)
    target_resources = [resource for resource in resources
                        if resource.ResourceFamilyName == family_name]
    return target_resources


def get_reservation_resources_by_model(sandbox, model_name):
    """
    :param Sandbox sandbox:
    :param str model_name:
    :return:
    """
    resources = get_reservation_resources(sandbox)
    target_resources = [resource for resource in resources
                        if resource.ResourceModelName == model_name]
    return target_resources


def get_routes_info(sandbox):
    """
    :param Sandbox sandbox:
    :return:
    """
    reservation_details = sandbox.automation_api.GetReservationDetails(reservationId=sandbox.id)
    routes_info = reservation_details.ReservationDescription.RequestedRoutesInfo
    return routes_info


def get_ip_from_device_name(sandbox, device_name):
    """
    :param Sandbox sandbox:
    :param str device_name: the name of the device passed in
    :return:
    """
    return [resource.FullAddress for resource in get_reservation_resources(sandbox)
            if resource.Name == device_name][0]
