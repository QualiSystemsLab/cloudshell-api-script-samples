"""
Module for storing convenience functions that wrap up automation_api functionality
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


def get_deployed_app_resources(sandbox):
    """
    :param Sandbox sandbox:
    :return:
    """
    reservation_details = sandbox.automation_api.GetReservationDetails(reservationId=sandbox.id)
    resources = reservation_details.ReservationDescription.Resources
    deployed_apps = [resource for resource in resources if resource.AppDetails]
    return deployed_apps
