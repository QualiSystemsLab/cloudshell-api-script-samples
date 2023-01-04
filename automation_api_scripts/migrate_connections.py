"""
migrate connections from one resource to a second
script assumes the target resource has same structure as source
"""
from typing import List


from cloudshell.api.cloudshell_api import CloudShellAPISession, ResourceInfo
from dataclasses import dataclass


@dataclass
class ConnectionData:
    source_resource: str
    target_resource: str


def _recursive_get_connections(children_resources: List[ResourceInfo]):
    """
    recursively get connections. No child resources is the base case
    :param list[ResourceInfo] children_resources:
    :param connections_list:
    :return:
    """
    result = []
    for resource in children_resources:
        connections = resource.Connections
        children = resource.ChildResources
        if not children:
            if connections:
                for connection in connections:
                    result.append(ConnectionData(resource.Name, connection.FullPath))
        else:
            _recursive_get_connections(children)
    return result


def get_connection_list(api: CloudShellAPISession, root_resource_name: str):
    root_details = api.GetResourceDetails(root_resource_name)
    root_children = root_details.ChildResources
    return _recursive_get_connections(root_children)


def migrate_connections(api: CloudShellAPISession, source_resource_name: str, target_resource_name: str) -> List[ConnectionData]:
    connections = get_connection_list(api, source_resource_name)
    for connection in connections:
        source_split = connection.source_resource.split("/")
        source_split[0] = target_resource_name
        new_source = "/".join(source_split)
        api.UpdatePhysicalConnection(resourceAFullPath=new_source,
                                     resourceBFullPath=connection.target_resource,
                                     overrideExistingConnections=True)
    new_connections = get_connection_list(api, target_resource_name)
    return new_connections


if __name__ == "__main__":
    SOURCE_RESOURCE = "DUT Mock 2"
    TARGET_RESOURCE = "mock_3"
    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
    new_connections = migrate_connections(api, SOURCE_RESOURCE, TARGET_RESOURCE)
    pass
