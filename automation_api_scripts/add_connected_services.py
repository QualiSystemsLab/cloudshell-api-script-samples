import math
import time

from cloudshell.api.cloudshell_api import CloudShellAPISession, SetConnectorRequest


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def add_connected_services(api: CloudShellAPISession, sb_id: str, source_resource_name: str, requested_services: int, service_model: str):
    col_height = 5
    x_offset = 350
    y_offset = 130
    top_offset = 50

    all_resource_positions = api.GetReservationResourcesPositions(reservationId=sb_id).ResourceDiagramLayouts
    target_pos_search = [x for x in all_resource_positions if x.ResourceName == source_resource_name]
    if not target_pos_search:
        raise ValueError(f"{source_resource_name} not found in position list")
    target_pos = target_pos_search[0]

    connected_services = get_connected_services(api, sb_id, source_resource_name, service_model)

    col_idx = len(connected_services) // col_height
    row_idx = len(connected_services) % col_height
    x_pos = target_pos.X + ((col_idx + 1) * x_offset)
    y_pos = top_offset + (row_idx * y_offset)

    start_range = len(connected_services) + 1
    end_range = start_range + requested_services
    services_to_add = []
    for i in range(start_range, end_range):
        curr_name = f"{source_resource_name}--{i}"
        api.AddServiceToReservation(reservationId=sb_id,
                                    serviceName=SERVICE_MODEL,
                                    alias=curr_name)
        api.SetReservationServicePosition(reservationId=sb_id,
                                          serviceAlias=curr_name,
                                          x=x_pos,
                                          y=y_pos)
        # time.sleep(3)
        services_to_add.append(curr_name)

        col_idx = i // col_height
        row_idx = i % col_height
        x_pos = target_pos.X + ((col_idx + 1) * x_offset)
        y_pos = top_offset + (row_idx * y_offset)

    connect_requests = [SetConnectorRequest(source_resource_name, x, "bi", "") for x in services_to_add]
    api.SetConnectorsInReservation(sb_id, connectors=connect_requests)


def get_connected_services(api: CloudShellAPISession, sb_id: str, source_resource: str, service_model: str):
    details = api.GetReservationDetails(sb_id, True).ReservationDescription
    sandbox_services = [x.Alias for x in details.Services if x.ServiceName == service_model]
    all_connectors = details.Connectors
    target_services = []
    for c in all_connectors:
        if source_resource == c.Source and c.Target in sandbox_services:
            target_services.append(c.Target)
        elif source_resource == c.Target and c.Source in sandbox_services:
            target_services.append(c.Source)
    return target_services


def delete_services(api: CloudShellAPISession, sb_id: str, service_model: str):
    all_services = api.GetReservationDetails(sb_id, True).ReservationDescription.Services
    target_services = [x for x in all_services if x.ServiceName == service_model]
    api.RemoveServicesFromReservation(sb_id, [x.Alias for x in target_services])


if __name__ == "__main__":
    SANDBOX_ID = "afb76801-f6f0-4281-91e8-53d11c8363f1"
    TARGET_RESOURCE = "test-linux-host"
    SERVICE_MODEL = "Ginger Agent"
    SERVICE_COUNT = 7

    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
    add_connected_services(api, SANDBOX_ID, TARGET_RESOURCE, SERVICE_COUNT, SERVICE_MODEL)
    # time.sleep(5)
    # delete_services(api, SANDBOX_ID, SERVICE_MODEL)
