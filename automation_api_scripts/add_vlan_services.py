from typing import List

from cloudshell.api.cloudshell_api import CloudShellAPISession, ResourceInfo, AttributeNameValue, SetConnectorRequest, \
    Connector
from dataclasses import dataclass


def add_vlan_manual_service(api: CloudShellAPISession, sandbox_id: str, input_vlan: str, alias: str = ""):
    service_attrs = [AttributeNameValue("VLAN ID", input_vlan)]
    api.AddServiceToReservation(reservationId=sandbox_id,
                                serviceName="VLAN Manual",
                                alias=alias,
                                attributes=service_attrs)


def set_vlan_connectors(api: CloudShellAPISession, sandbox_id: str, source_port: str, target_port: str, input_vlan: str,
                        service_alias: str):
    connector_requests = [
        SetConnectorRequest(SourceResourceFullName=service_alias,
                            TargetResourceFullName=source_port,
                            Direction="bi",
                            Alias=input_vlan),
        SetConnectorRequest(SourceResourceFullName=service_alias,
                            TargetResourceFullName=target_port,
                            Direction="bi",
                            Alias=input_vlan)
    ]
    api.SetConnectorsInReservation(reservationId=sandbox_id,
                                   connectors=connector_requests)
    connect_all_vlan_manual(api, sandbox_id, service_alias)


def connect_all_vlan_manual(api: CloudShellAPISession, sandbox_id: str, service_alias):
    api.ExecuteCommand(reservationId=sandbox_id,
                       targetName=service_alias,
                       targetType="Service",
                       commandName="Vlan Service Connect All",
                       printOutput=True)


if __name__ == "__main__":
    DUT1 = "DUT Mock 1/Port 1"
    DUT2 = "DUT Mock 2/Port 1"
    SANDBOX_ID = "5d226888-9dd1-4157-8411-64b06bcbe7e0"
    VLAN_MANUAL_MODEL = "VLAN Manual"
    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
    # add_vlan_manual_service(api, SANDBOX_ID, "6", "test_service")
    set_vlan_connectors(api, SANDBOX_ID, DUT1, DUT2, "5", "test_service 1")
    pass
