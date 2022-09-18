import argparse
import json
import winrm

from dataclasses import dataclass
from typing import List
from quali_api_helper import QualiAPISession


@dataclass
class ConfigExecutionServer:
    es_name: str  # name of es in cloudshell
    user: str
    password: str
    address: str


def get_cli_server_list() -> List[str]:
    CLI = argparse.ArgumentParser()
    CLI.add_argument("--servers", nargs="*", type=str)
    args = CLI.parse_args()
    return args.servers


def get_target_config_servers(target_servers: List[str], config_servers: List[ConfigExecutionServer]):
    target_config_servers = []
    conf_server_names = [x.es_name for x in config_servers]
    conf_servers_dict = {x.es_name: x for x in config_servers}
    for server in target_servers:
        if server not in conf_server_names:
            raise ValueError(f"can't find target server {server} in config server json")
        target_config_servers.append(conf_servers_dict[server])
    return target_config_servers


def validate_servers_not_running(api: QualiAPISession, target_servers: List[str]):
    for server in target_servers:
        server_details = api.get_execution_server_details(server)
        running_jobs = server_details["running"]
        if running_jobs > 0:
            raise ValueError(f"Server {server} has {running_jobs} running jobs. Stopping")


def run_git_flow(config_servers: List[ConfigExecutionServer], remote_repo_path: str):
    for server in config_servers:
        session = winrm.Session(target=server.address, auth=(server.user, server.password))
        session.run_ps(f"Test-NetConnection -Computername {server.address} -Port 5985")
        session.run_ps(f"Test-WSMAN {server.address}")
        session.run_ps(f"Set-Location {remote_repo_path};git pull")


if __name__ == "__main__":
    api = QualiAPISession("localhost", "admin", "admin")
    REMOTE_REPO_PATH = "C:/testshell-repo/Tests"
    with open("servers.json") as f:
        data = json.load(f)
    config_servers = [ConfigExecutionServer(x["hostname"], x["user"], x["password"], x["address"]) for x in data]
    target_servers = get_cli_server_list()
    target_config_servers = get_target_config_servers(target_servers, config_servers)
    validate_servers_not_running(api, target_servers)
    run_git_flow(target_config_servers, REMOTE_REPO_PATH)
