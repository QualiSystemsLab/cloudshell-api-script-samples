from cloudshell.helpers.scripts.cloudshell_scripts_helpers import get_reservation_context_details, get_api_session, \
    get_resource_context_details
from cloudshell.api.cloudshell_api import Connector


def _get_connected_resource(connector: Connector, root_resource_name: str):
    if connector.Source.startswith(root_resource_name):
        target_side = connector.Source
    elif connector.Target.startswith(root_resource_name):
        target_side = connector.Target
    else:
        raise ValueError(f"root resource {root_resource_name} not present in Source or Target of connector")

    connected_port = target_side.split("/")[-1]
    return connected_port


def get_port_from_connector_alias(target_alias: str):
    api = get_api_session()
    sb_details = get_reservation_context_details()
    sb_id = sb_details.id

    resource_details = get_resource_context_details()
    resource_name = resource_details.name

    api.WriteMessageToReservationOutput(reservationId=sb_id,
                                        message=f"Searching for port connected to alias '{target_alias}'...")

    reservation_details = api.GetReservationDetails(reservationId=sb_id, disableCache=True).ReservationDescription
    connectors = reservation_details.Connectors
    target_connector_search = [x for x in connectors if x.Alias == target_alias]
    if not target_connector_search:
        raise ValueError(f"Connector with Alias {target_alias} not found")
    target_connector = target_connector_search[0]
    connected_resource = _get_connected_resource(target_connector, resource_name)

    # printing to std_out will be the return output of resource scripts
    print(connected_resource)
