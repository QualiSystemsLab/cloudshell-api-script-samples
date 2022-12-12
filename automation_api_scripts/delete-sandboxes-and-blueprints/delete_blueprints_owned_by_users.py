"""
The general use case here is to delete blueprints owned by a specific user
Perhaps you want to delete user from DB, or just want to remove their data
"""
import json

import sys
from argparse import ArgumentParser
from common import add_cs_server_args, get_cloudshell_api, get_regular_blueprints_owned_by_users, add_target_user_arg, \
    validate_cloudshell_users
import constants as const

parser = ArgumentParser(prog="Delete ALL blueprints",
                        description="Automation API script to delete blueprints")
add_cs_server_args(parser)
add_target_user_arg(parser)

# unpack args
args_dict = vars(parser.parse_args())
server = args_dict[const.SERVER_KEY]
user = args_dict[const.USER_KEY]
password = args_dict[const.PASSWORD_KEY]
target_users = args_dict[const.TARGET_USERS_KEY]

api = get_cloudshell_api(server, user, password)
validate_cloudshell_users(api, target_users)
target_blueprints = get_regular_blueprints_owned_by_users(api, target_users)

if not target_blueprints:
    print("No blueprints found. Stopping.")
    sys.exit(0)

print("Deleting ALL blueprints owned by target users...")
failed = []
for curr_bp in target_blueprints:
    print(f"Deleting blueprint '{curr_bp.Name}'")
    try:
        api.DeleteTopology(topologyFullPath=curr_bp.Name)
    except Exception as e:
        print(f"Error deleting blueprint '{curr_bp.Name}'. Exception - \n{type(e).__name__}: {str(e)}")
        print("===============")
        failed.append(curr_bp.Name)


if failed:
    raise Exception(f"Failed blueprint deletions:\n{json.dumps(failed, indent=4)}")

print("Delete blueprints for target users script done.")
