import json
from typing import List

import sys
from argparse import ArgumentParser
from common import add_cs_server_args, add_time_range_args, get_cloudshell_api, get_all_historical_sandboxes, \
    add_target_user_arg, validate_cloudshell_users
import constants as const
from cloudshell.api.cloudshell_api import ReservationShortInfo

parser = ArgumentParser(prog="Delete sandboxes for target users",
                        description="Automation API script to delete sandboxes")
add_cs_server_args(parser)
add_time_range_args(parser)
add_target_user_arg(parser)

# unpack args
args_dict = vars(parser.parse_args())
server = args_dict[const.SERVER_KEY]
user = args_dict[const.USER_KEY]
password = args_dict[const.PASSWORD_KEY]
from_time = args_dict[const.FROM_KEY]
until_time = args_dict[const.UNTIL_KEY]
target_users = args_dict[const.TARGET_USERS_KEY]

api = get_cloudshell_api(server, user, password)
validate_cloudshell_users(api, target_users)
all_historical_sandboxes = get_all_historical_sandboxes(api, from_time, until_time)

if not all_historical_sandboxes:
    print("No historical sandboxes found. Stopping.")
    sys.exit(0)


def is_user_in_sandbox(sandbox: ReservationShortInfo, target_users: List[str]):
    if sandbox.Owner in target_users:
        return True
    for curr_user in sandbox.PermittedUsers:
        if curr_user in target_users:
            return True
    return False


target_user_sandboxes = [x for x in all_historical_sandboxes if is_user_in_sandbox(x, target_users)]
if not target_user_sandboxes:
    print("No sandboxes found with target users associated. Stopping.")
    sys.exit(0)

print("Deleting historical sandboxes associated with target users...")
failed = []
for sandbox in target_user_sandboxes:
    print(f"Deleting sandbox '{sandbox.Id}'")
    try:
        api.DeleteReservation(sandbox.Id)
    except Exception as e:
        print(f"Error deleting sandbox '{sandbox.Id}'. Exception - \n{type(e).__name__}: {str(e)}")
        print("===============")
        failed.append(sandbox.Id)

if failed:
    raise Exception(f"Failed sandbox deletions:\n{json.dumps(failed, indent=4)}")

print("Delete sandboxes for target users done.")
