import json
from typing import List

from argparse import ArgumentParser
import sys
from cloudshell.api.cloudshell_api import CloudShellAPISession, ReservationShortInfo, TopologyInfo

import constants as const


def add_cs_server_args(parser: ArgumentParser):
    parser.add_argument('-s', f'--{const.SERVER_KEY}', required=True, help="Cloudshell Server User")
    parser.add_argument('-u', f'--{const.USER_KEY}', required=True, help="Cloudshell Server Password")
    parser.add_argument('-p', f'--{const.PASSWORD_KEY}', required=True, help="Cloudshell Server IP or DNS name")


def add_time_range_args(parser: ArgumentParser):
    parser.add_argument(f'--{const.FROM_KEY}', help="start range. format MM/DD/YYYY HH:MM, ex. 01/01/2015 00:00",
                        default="01/01/2015 00:00")
    parser.add_argument(f'--{const.UNTIL_KEY}', help="end range. format MM/DD/YYYY HH:MM, ex. 01/01/2025 00:00",
                        default="01/01/2025 00:00")


def add_target_user_arg(parser: ArgumentParser):
    parser.add_argument(f'--{const.TARGET_USERS_KEY}',
                        help="list of space separated cloudshell users. Example: user1 user2 user3.",
                        required=True)


def _prompt_to_delete(prompt_text):
    # raw_input returns the empty string for "enter"
    yes = {'yes', 'y', 'ye', ''}
    no = {'no', 'n'}

    choice = input(prompt_text).lower()

    if choice in yes:
        print("Starting script..")
        return
    elif choice in no:
        print("Ending script")
        sys.exit(0)
    else:
        print("Please respond with 'yes' or 'no'")
        sys.exit(0)


def all_sandbox_delete_prompt(from_time, until_time):
    prompt = f"Are you sure you want to delete ALL sandboxes in time range {from_time} - {until_time}? [y/n]"
    _prompt_to_delete(prompt)


def all_blueprint_delete_prompt():
    prompt = "Are you sure you want to delete ALL blueprints? [y/n]"
    _prompt_to_delete(prompt)


def get_cloudshell_api(server, user, password) -> CloudShellAPISession:
    try:
        api = CloudShellAPISession(host=server, username=user, password=password, domain="Global")
    except Exception as e:
        print(f"Issue getting cloudshell API session. {type(e).__name__}: {str(e)}")
        raise
    return api


def get_all_historical_sandboxes(api: CloudShellAPISession, from_time: str, until_time: str) -> List[
    ReservationShortInfo]:
    try:
        all_sandboxes = api.GetScheduledReservations(fromTime=from_time, untilTime=until_time).Reservations
    except Exception as e:
        print(f"Issue getting sandboxes. {type(e).__name__}: {str(e)}")
        raise
    historical_sandboxes = [x for x in all_sandboxes if x.Status == "Completed"]
    return historical_sandboxes


def get_all_regular_blueprints(api: CloudShellAPISession) -> List[TopologyInfo]:
    all_blueprints = api.GetTopologiesByCategory().Topologies
    results = []
    for curr_bp in all_blueprints:
        details = api.GetTopologyDetails(topologyFullPath=curr_bp)
        if details.Type == "Regular":
            results.append(details)
    return results


def get_regular_blueprints_owned_by_users(api: CloudShellAPISession, owners: List[str]) -> List[TopologyInfo]:
    all_blueprints = api.GetTopologiesByCategory().Topologies
    results = []
    for curr_bp in all_blueprints:
        details = api.GetTopologyDetails(topologyFullPath=curr_bp)
        if details.Type == "Regular":
            for curr_owner in owners:
                if curr_owner == details.Owner:
                    results.append(details)
    return results


def validate_cloudshell_users(api: CloudShellAPISession, users: List[str]):
    failed = []
    for curr_user in users:
        try:
            api.GetUserDetails(curr_user)
        except Exception as e:
            failed.append(curr_user)
    if failed:
        raise Exception(f"Invalid cloudshell users passed:\n{json.dumps(failed, indent=4)}")

if __name__ == "__main__":
    api = CloudShellAPISession("localhost", "admin", "admin", "Global")
    get_all_historical_sandboxes(api, "01/01/2018 00:00", "01/01/2022 00:00")
    pass
