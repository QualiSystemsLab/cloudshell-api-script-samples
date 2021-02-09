import time
from helper_code.sandbox_print_helpers import *
import helper_code.automation_api_helpers as api_help
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_help
import os
import sys
from DEBUG_GLOBALS import DEBUG_MODE

SLEEP_TIME = 30


# ========== Primary Function ==========
def first_module_flow():
    """
    Functions passed into orchestration flow MUST have (sandbox, components) signature
    :param Sandbox sandbox:
    :param components
    :return:
    """
    # script helpers to pull in sandbox details, resource details, and api session
    sb_context = script_help.get_reservation_context_details()
    resource_details = script_help.get_resource_context_details()
    api = script_help.get_api_session()
    res_id = sb_context.id
    ip = resource_details.address
    resource_name = resource_details.name

    warn_print(api, res_id, "'{}' command started. Sleeping {} seconds...".format(resource_name, str(SLEEP_TIME)))

    # exception testing
    # if resource_name in ["mock_1", "mock_2"]:
    #     raise Exception("RESOURCE '{}' got messed up".format(resource_name))
    # raise Exception("RESOURCE '{}' got messed up".format(resource_name))

    start_time = time.time()

    # simulate computation
    time.sleep(SLEEP_TIME)

    duration = time.time() - start_time
    print("RESOURCE: {}, DURATION: {}".format(resource_name, duration))
