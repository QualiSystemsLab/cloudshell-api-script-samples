from cloudshell.api.cloudshell_api import CloudShellAPISession
from typing import List


def exclude_ports(api: CloudShellAPISession, target_ports: List[str]):
    api.ExcludeResources(target_ports)


def include_ports(api: CloudShellAPISession, target_ports: List[str]):
    api.IncludeResources(target_ports)


if __name__ == "__main__":
    api = CloudShellAPISession("localhost", "admin", "admin", "Global")
    TARGET_PORTS = ["cl-app-polatis/Port 001", "cl-app-polatis/Port 002"]
    # exclude_ports(api, TARGET_PORTS)
    include_ports(api, TARGET_PORTS)