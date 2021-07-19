import json

import sys
from argparse import ArgumentParser
from common import add_cs_server_args, get_cloudshell_api, all_blueprint_delete_prompt, get_all_regular_blueprints
import constants as const

parser = ArgumentParser(prog="Delete ALL blueprints",
                        description="Automation API script to delete blueprints")
add_cs_server_args(parser)

# unpack args
args_dict = vars(parser.parse_args())
server = args_dict[const.SERVER_KEY]
user = args_dict[const.USER_KEY]
password = args_dict[const.PASSWORD_KEY]

all_blueprint_delete_prompt()
api = get_cloudshell_api(server, user, password)
all_blueprints = get_all_regular_blueprints(api)

if not all_blueprints:
    print("No blueprints found. Stopping.")
    sys.exit(0)

print("Deleting ALL blueprints...")
failed = []
for curr_bp in all_blueprints:
    print(f"Deleting blueprint '{curr_bp.Name}'")
    try:
        api.DeleteTopology(topologyFullPath=curr_bp.Name)
    except Exception as e:
        print(f"Error deleting blueprint '{curr_bp.Name}'. Exception - \n{type(e).__name__}: {str(e)}")
        print("===============")
        failed.append(curr_bp.Name)

if failed:
    raise Exception(f"Failed blueprint deletions:\n{json.dumps(failed, indent=4)}")

print("Delete blueprints script done.")
