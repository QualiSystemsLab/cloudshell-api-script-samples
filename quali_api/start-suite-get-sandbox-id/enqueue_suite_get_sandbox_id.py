"""
This script is a method to obtain sandbox id of newly formed job.
Methodology is to pass in a UUID as global input, then to query sandbox id for sandbox with matching input value
NOTE: Sandbox Api server may not be hosted on quali server, it is typically hosted together with Portal server
https://help.quali.com/Online%20Help/0.0/Portal/Content/IG/Overview/cs-reqd-ports.htm?Highlight=ports
"""
import time

from quali_api_wrapper import QualiAPISession
from sandbox_rest_api import SandboxRest
import json
from timeit import default_timer


def get_sandbox_id_from_job(quali_api: QualiAPISession, sandbox_api: SandboxRest,
                            suite_data: dict, global_input_name: str, global_input_value: str):
    print(f"starting new job, passing '{global_input_value}' as custom UUID")

    # pass in custom global value - assuming only 1 job per suite
    global_inputs = suite_data["JobsDetails"][0]["Topology"]["GlobalInputs"]
    target_input = [x for x in global_inputs if x["Name"] == global_input_name][0]
    target_input["Value"] = global_input_value

    # start new suite with quali pai
    suite_id = quali_api.enqueue_suite(suite_data=suite_data)
    print(f"suite started: {suite_id}")

    # give DB a few seconds to propagate new sandbox
    time.sleep(3)

    # query sandbox api for matching sandbox
    print("searching for job's sandbox...")
    start = default_timer()
    all_sandboxes = sandbox_api.get_sandboxes()
    for sandbox in all_sandboxes:
        sandbox_details = sandbox_api.get_sandbox_data(sandbox_id=sandbox["id"])
        global_inputs = sandbox_details["parameters"]
        target_global = [x for x in global_inputs if x["Name"] == global_input_name]
        if not target_global:
            continue
        target_value = target_global[0]["Value"]
        if target_value == global_input_value:
            print(f"sandbox id found after '{default_timer() - start}' seconds")
            return sandbox["id"]


if __name__ == "__main__":
    SUITE_JSON_PATH = 'suite_data.json'
    TARGET_GLOBAL_PARAM_NAME = "my_uuid"
    TARGET_GLOBAL_PARAM_VALUE = "123456789"

    quali_api = QualiAPISession(host="localhost", username="admin", password="admin", domain="Global")
    sandbox_api = SandboxRest(server="localhost", username="admin", password="admin", domain="Global")

    # read in suite json
    with open(SUITE_JSON_PATH) as handle:
        suite_data_dict = json.loads(handle.read())

    sandbox_id = get_sandbox_id_from_job(quali_api=quali_api,
                                         sandbox_api=sandbox_api,
                                         suite_data=suite_data_dict,
                                         global_input_name=TARGET_GLOBAL_PARAM_NAME,
                                         global_input_value=TARGET_GLOBAL_PARAM_VALUE)
    print(f"sandbox id: {sandbox_id}")
