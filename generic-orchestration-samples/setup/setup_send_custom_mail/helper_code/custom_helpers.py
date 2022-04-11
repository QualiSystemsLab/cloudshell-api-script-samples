"""
Module for storing convenience functions that wrap up automation_api functionality
A general rule: If the function is generic enough to be used across every sandbox, this is a good home for it
"""

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
    resources = reservation_details.ReservationDescription.Resources
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


def connect_routes(sandbox, mapping_type="bi", print_output=False):
    """
    :param Sandbox sandbox:
    :param bool print_output: flag to turn print output on/off
    :param str mapping_type: set mapping type to bidirectional / unidirectional ["bi", "uni"]
    :return:
    """
    routes = get_routes_info(sandbox)
    if print_output:
        sb_print(sandbox, "===== Connecting All Routes =====")

    if routes:
        if print_output:
            sb_print(sandbox, "SOURCE -----> TARGET")
        for route in routes:
            sandbox.automation_api.ConnectRoutesInReservation(reservationId=sandbox.id,
                                                              endpoints=[route.Source, route.Target],
                                                              mappingType=mapping_type)
            if print_output:
                sb_print(sandbox, route.Source + " -----> " + route.Target)
    else:
        if print_output:
            sb_print(sandbox, "No routes were found in this sandbox")
    if print_output:
        sb_print(sandbox, "==========")
