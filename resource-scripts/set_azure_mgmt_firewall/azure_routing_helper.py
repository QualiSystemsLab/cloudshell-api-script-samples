from typing import List, Dict

from cloudshell.api.cloudshell_api import InputNameValue, CloudShellAPISession, Connector, VmDetailsNetworkInterface
import json

from cloudshell.helpers.sandbox_reporter.reporter import SandboxReporter


class SetAzureRoutesError(Exception):
    pass


class Route:
    def __init__(self, name: str, address_prefix: str, next_hop_address: str, next_hop_type="VirtualAppliance"):
        self.name = name.replace(" ", "_")
        self.address_prefix = address_prefix
        self.next_hop_address = next_hop_address
        self.next_hop_type = next_hop_type


class RouteTable:
    def __init__(self, name: str):
        self.name = name.replace(" ", "_")
        self.subnets: List[str] = []
        self.routes: List[Route] = []


class AzureRouteTableRequest:
    """
    Sample JSON structure to build
    {
        "route_tables": [
            {
                "name": "myRouteTable1",
                "subnets": [
                    "subnetId1",
                    "subnetId2"
                ],
                "routes": [
                    {
                        "name": "myRoute1",
                        "address_prefix": "10.0.1.0/28",
                        "next_hop_type": "VirtualAppliance",
                        "next_hop_address": "10.0.1.15"
                    }
                ]
            },
            {
                "name": "myRouteTable2",
                "subnets": [
                    "subnetId3",
                    "subnetId4"
                ],
                "routes": [
                    {
                        "name": "myRoute2",
                        "address_prefix": "10.0.1.0/28",
                        "next_hop_type": "VirtualAppliance",
                        "next_hop_address": "10.0.1.15"
                    }
                ]
            }
        ]
    }
    """

    def __init__(self):
        self.route_tables: List[RouteTable] = []

    def get_json(self):
        return json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))

    def get_pretty_json(self):
        return json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)), indent=4)


def _get_connector_endpoints(resource_name: str, resource_connectors: List[Connector]) -> List[str]:
    """ get back a list of connector endpoints from the sandbox details Connectors """
    connector_endpoints = []
    for connector in resource_connectors:
        if connector.Source == resource_name or connector.Target == resource_name:
            if connector.Source == resource_name:
                connector_endpoints.append(connector.Target)
            else:
                connector_endpoints.append(connector.Source)
    return connector_endpoints


def _build_gateway_request_obj(api: CloudShellAPISession, res_id: str, target_resource_name: str):
    """
    treats input resource name as central routing gateway when building route table

    for sample topology:
    subnetA -> VA
    subnet B - > VA
    subnet C -> VA

    create routes for:
    subnetA -> subnetB
    subnetA -> subnetC
    subnetB -> subnetA
    subnetB -> subnetC
    subnetC -> subnetA
    subnetC -> subnetB
    """
    request_obj = AzureRouteTableRequest()

    # Network ID in VM Details matches subnet ID, so setting up dict for easy access
    resource_details = api.GetResourceDetails(target_resource_name)
    if not resource_details.VmDetails:
        raise SetAzureRoutesError(f"No VM Details found for {resource_details.Name}")
    network_id_map: Dict[str, VmDetailsNetworkInterface] = {x.NetworkId: x for x in resource_details.VmDetails.NetworkData}

    # pull all subnets in sandbox and find the ones connected to Virtual Appliance
    sb_details = api.GetReservationDetails(res_id, True).ReservationDescription
    connectors = sb_details.Connectors
    all_services = sb_details.Services
    connector_endpoints = _get_connector_endpoints(target_resource_name, connectors)
    subnet_services = [s for s in all_services if "subnet" in s.ServiceName.lower()]
    subnet_service_names = [s.Alias for s in subnet_services]
    subnet_endpoint_names = list(set(connector_endpoints).intersection(set(subnet_service_names)))
    connected_subnet_services = [s for s in subnet_services if s.Alias in subnet_endpoint_names]

    # iterate over connected services and add route to the other connected services
    for source_subnet in connected_subnet_services:
        subnet_id = [attr.Value for attr in source_subnet.Attributes if "subnet id" in attr.Name.lower()][0]
        network_additional_data = network_id_map[subnet_id].AdditionalData
        interface_ip = [x for x in network_additional_data if x.Name.lower() == "ip"][0].Value
        target_subnet_services = [s for s in connected_subnet_services if s.Alias != source_subnet.Alias]
        route_table_name = "{}-Source-RouteTable".format(source_subnet.Alias)
        curr_route_table = RouteTable(name=route_table_name)
        curr_route_table.subnets.append(subnet_id)
        request_obj.route_tables.append(curr_route_table)
        for target_service in target_subnet_services:
            route_name = f"Source__{source_subnet.Alias}-to-Target__{target_service.Alias}"
            target_cidr = [x for x in target_service.Attributes if "allocated cidr" in x.Name.lower()][0].Value
            if not target_cidr:
                raise Exception(f"Allocated CIDR not populated on service '{target_service.Alias}'")
            curr_route = Route(name=route_name,
                               address_prefix=target_cidr,
                               next_hop_address=interface_ip)
            curr_route_table.routes.append(curr_route)
    return request_obj


def _send_route_table_request(api, res_id, azure_clp_resource, request_json):
    """
    convenience wrapper for the command
    :param CloudShellAPISession api:
    :param str res_id:
    :param str azure_clp_resource:
    :param str request_json:
    """
    return api.ExecuteCommand(reservationId=res_id,
                              targetName=azure_clp_resource,
                              targetType="Resource",
                              commandName="CreateRouteTables",
                              commandInputs=[InputNameValue("request", request_json)],
                              printOutput=False).Output


def set_virtual_appliance_routes(va_resource_name: str, clp_resource_name: str, api: CloudShellAPISession, res_id: str,
                                 reporter: SandboxReporter) -> str:
    try:
        azure_gateway_request_obj = _build_gateway_request_obj(api, res_id, va_resource_name)
    except Exception as e:
        exc_msg = "Issue building Azure routing request object: {}".format(str(e))
        reporter.error(exc_msg)
        raise SetAzureRoutesError(exc_msg)

    request_json = azure_gateway_request_obj.get_json()
    pretty_json = azure_gateway_request_obj.get_pretty_json()

    reporter.warning("=== Sending Azure Route Tables Request ===")
    reporter.info(pretty_json)
    try:
        output = _send_route_table_request(api, res_id, clp_resource_name, request_json)
    except Exception as e:
        err_msg = f"Issue sending Azure route table request. {type(e).__name__}: {str(e)}"
        reporter.error(err_msg)
        raise SetAzureRoutesError(err_msg)
    return output
