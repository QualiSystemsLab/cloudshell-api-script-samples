import time
from typing import List

from cloudshell.api.cloudshell_api import CloudShellAPISession, SetConnectorRequest, AttributeNameValue, \
    ResourceDiagramLayoutInfo
from dataclasses import dataclass, field


@dataclass
class AddServiceRequest:
    """ attributes are optional - default to empty list """
    service_model: str
    service_attrs: List[AttributeNameValue] = field(default_factory=lambda: [])


def add_connected_services(api: CloudShellAPISession, sb_id: str, source_resource_name: str,
                           requested_services_data: List[AddServiceRequest], connected_count: int = 0):
    """
    connected count is to statefully calculate the matrix index for appending new services
    if you pass 0, it will add from start of matrix
    """
    col_height = 5
    x_offset = 350
    y_offset = 130
    top_offset = 50

    source_resource_pos = get_resource_position(api, sb_id, source_resource_name)

    # init (x,y) coordinates
    col_idx = connected_count // col_height
    row_idx = connected_count % col_height
    x_pos = source_resource_pos.X + ((col_idx + 1) * x_offset)
    y_pos = top_offset + (row_idx * y_offset)

    matrix_idx = connected_count + 1
    services_to_connect = []
    for req in requested_services_data:
        curr_name = f"{source_resource_name}--{matrix_idx}"
        services_to_connect.append(curr_name)

        api.AddServiceToReservation(reservationId=sb_id,
                                    serviceName=req.service_model,
                                    alias=curr_name,
                                    attributes=req.service_attrs)
        api.SetReservationServicePosition(reservationId=sb_id,
                                          serviceAlias=curr_name,
                                          x=x_pos,
                                          y=y_pos)
        # update (x,y)
        col_idx = matrix_idx // col_height
        row_idx = matrix_idx % col_height
        x_pos = source_resource_pos.X + ((col_idx + 1) * x_offset)
        y_pos = top_offset + (row_idx * y_offset)
        matrix_idx += 1

    connect_requests = [SetConnectorRequest(source_resource_name, x, "bi", "") for x in services_to_connect]
    api.SetConnectorsInReservation(sb_id, connectors=connect_requests)


def get_resource_position(api, sb_id, source_resource_name) -> ResourceDiagramLayoutInfo:
    all_resource_positions = api.GetReservationResourcesPositions(reservationId=sb_id).ResourceDiagramLayouts
    target_pos_search = [x for x in all_resource_positions if x.ResourceName == source_resource_name]
    if not target_pos_search:
        raise ValueError(f"{source_resource_name} not found in position list")
    return target_pos_search[0]


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
    """ helper to clean up services """
    all_services = api.GetReservationDetails(sb_id, True).ReservationDescription.Services
    target_services = [x for x in all_services if x.ServiceName == service_model]
    api.RemoveServicesFromReservation(sb_id, [x.Alias for x in target_services])


if __name__ == "__main__":
    SANDBOX_ID = "26714fd7-e933-4b09-b77f-cd02da98e855"
    TARGET_RESOURCE = "test-linux-host"
    SERVICE_MODEL = "Ginger Agent"
    SERVICE_COUNT = 7
    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")

    connected_services = get_connected_services(api, SANDBOX_ID, TARGET_RESOURCE, SERVICE_MODEL)
    service_requests = [AddServiceRequest(SERVICE_MODEL) for x in range(SERVICE_COUNT)]
    add_connected_services(api, SANDBOX_ID, TARGET_RESOURCE, service_requests, connected_count=len(connected_services))
    time.sleep(5)
    delete_services(api, SANDBOX_ID, SERVICE_MODEL)
