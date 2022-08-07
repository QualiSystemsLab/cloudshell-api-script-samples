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


if __name__ == "__main__":
    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
    connections = get_connection_list(api, "DUT Mock 1")
    pass
