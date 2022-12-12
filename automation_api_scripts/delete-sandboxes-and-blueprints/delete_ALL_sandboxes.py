"""
Caution, this will delete ALL historical sandboxes
This is for the use case where customers do not wish to store historical data of the environments in their sandbox
script has "are you sure" prompt added to CLI usage
USE WITH CAUTION
"""
import json

import sys
from argparse import ArgumentParser
from common import add_cs_server_args, add_time_range_args, get_cloudshell_api, get_all_historical_sandboxes, \
    all_sandbox_delete_prompt
import constants as const

parser = ArgumentParser(prog="Delete ALL sandboxes",
                        description="Automation API script to delete sandboxes")
add_cs_server_args(parser)
add_time_range_args(parser)

# unpack args
args_dict = vars(parser.parse_args())
server = args_dict[const.SERVER_KEY]
user = args_dict[const.USER_KEY]
password = args_dict[const.PASSWORD_KEY]
from_time = args_dict[const.FROM_KEY]
until_time = args_dict[const.UNTIL_KEY]

all_sandbox_delete_prompt(from_time, until_time)
api = get_cloudshell_api(server, user, password)
all_historical_sandboxes = get_all_historical_sandboxes(api, from_time, until_time)

if not all_historical_sandboxes:
    print("No historical sandboxes found. Stopping.")
    sys.exit(0)

print("Deleting ALL historical Sandboxes...")
failed = []
for sandbox in all_historical_sandboxes:
    print(f"Deleting sandbox '{sandbox.Id}'")
    try:
        api.DeleteReservation(sandbox.Id)
    except Exception as e:
        print(f"Error deleting sandbox '{sandbox.Id}'. Exception - \n{type(e).__name__}: {str(e)}")
        print("===============")
        failed.append(sandbox.Id)


if failed:
    raise Exception(f"Failed sandbox deletions:\n{json.dumps(failed, indent=4)}")

print("Delete sandboxes script done.")
