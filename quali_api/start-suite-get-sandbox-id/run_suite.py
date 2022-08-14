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
POLLING_FREQUENCY_SECONDS = 10


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
        details = api.get_suite_details(suite_id)
        status = details["SuiteStatus"]
        job = details['JobsDetails'][0]
        tests = job['Tests']
        running_test = None
        for test in tests:
            if test["State"] == "Running":
                running_test = test
        if running_test:
            test_path = running_test["TestPath"]
            print(f"Current running test: {test_path}")
        else:
            print("no running test data now")
        time.sleep(POLLING_FREQUENCY_SECONDS)

    time.sleep(5)
    running_seconds = int(default_timer() - start)
    print(f"Suite {suite_id} completed with status {status} after {running_seconds} seconds.")
    details = api.get_suite_details(suite_id)
    result = details["SuiteResult"]
    print(f"Suite Result: {result}")
    job = details['JobsDetails'][0]
    tests = job['Tests']
    for test in tests:
        test_path = test["TestPath"]
        test_result = test["Result"]
        report_link = test["ReportLink"]
        print(f"Test Path '{test_path}', Result: {test_result}")
        print(f"Report Link: {report_link}")
        print("=====")
    print("===============")
    print(f"Full Suite details: {json.dumps(details, indent=4)}")
    print("Suite Done!")


if __name__ == "__main__":
    SUITE_JSON_PATH = 'suite_data.json'
    quali_api = QualiAPISession(host="localhost", username="admin", password="admin", domain="Global")

    # read in template data and run
    suite_details = quali_api.get_suite_template_details("natti suite")
    suite_details['SuiteName'] = "natti test"
    job = suite_details['JobsDetails'][0]
    tests = job['Tests']
    for test in tests:
        params = test['Parameters']
        input_1_search = [x for x in params if x['ParameterName'] == "input_1"]
        if not input_1_search:
            raise ValueError("can't find target input in test")
        input_1 = input_1_search[0]
        input_1['ParameterValue'] = "natti input"

    run_suite_and_poll(quali_api, suite_details)
    pass

    # run from static file example
    # with open(SUITE_JSON_PATH) as handle:
    #     suite_data_dict = json.loads(handle.read())
    #
    # run_suite_and_poll(quali_api, suite_data_dict)
