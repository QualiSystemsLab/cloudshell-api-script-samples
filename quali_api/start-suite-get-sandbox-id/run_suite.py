"""
This script is a method to obtain sandbox id of newly formed job.
Methodology is to pass in a UUID as global input, then to query sandbox id for sandbox with matching input value
NOTE: Sandbox Api server may not be hosted on quali server, it is typically hosted together with Portal server
https://help.quali.com/Online%20Help/0.0/Portal/Content/IG/Overview/cs-reqd-ports.htm?Highlight=ports
"""
import time

from quali_api import QualiAPISession, SUITE_FINISHED_STATES
import json
from timeit import default_timer

MAX_POLLING_SECONDS = 900


def run_suite_and_poll(api: QualiAPISession, suite_data: dict):
    print(f"starting suite...")
    suite_id = api.enqueue_suite(suite_data)
    status = api.get_suite_details(suite_id)["SuiteStatus"]

    # poll status
    start = default_timer()
    while status not in SUITE_FINISHED_STATES:
        running_time = default_timer() - start
        if running_time > MAX_POLLING_SECONDS:
            raise Exception(f"Polling reached timeout of {MAX_POLLING_SECONDS} seconds")
        status = api.get_suite_details(suite_id)["SuiteStatus"]
        print(f"current status: {status}")
        time.sleep(10)

    running_seconds = int(default_timer() - start)
    print(f"Suite {suite_id} completed with status {status} after {running_seconds} seconds.")
    details = api.get_suite_details(suite_id)
    result = details["SuiteResult"]
    print(f"Suite Result: {result}")


if __name__ == "__main__":
    SUITE_JSON_PATH = 'suite_data.json'
    quali_api = QualiAPISession(host="localhost", username="admin", password="admin", domain="Global")

    with open(SUITE_JSON_PATH) as handle:
        suite_data_dict = json.loads(handle.read())

    run_suite_and_poll(quali_api, suite_data_dict)
