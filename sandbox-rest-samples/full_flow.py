"""
sample script showing full flow of reserving sandbox, running some commands, and ending
See docs for rest client docs
https://github.com/QualiSystemsLab/Sandbox-API-Python

See help for more general info
https://help.quali.com/Online%20Help/0.0/Portal/Content/API/CS-Snbx-API-Topic.htm?Highlight=sandbox%20api
"""
import json
import time
from time import sleep
from timeit import default_timer

from cloudshell.sandbox_rest.sandbox_api import SandboxRestApiSession  # pip install cloudshell-sandbox-rest


def start_sandbox(api: SandboxRestApiSession, blueprint_name: str, timeout_seconds=1200) -> str:
    print("starting sandbox...")
    response = api.start_sandbox(blueprint_id=blueprint_name)
    print("sandbox started. Polling Setup...")
    sandbox_id = response["id"]
    res = api.get_sandbox_details(sandbox_id)
    state = res["state"]
    start = default_timer()
    while state != "Ready":
        res = api.get_sandbox_details(sandbox_id)
        state = res["state"]
        print(f"Sandbox state: {state}")
        sleep(10)
        setup_time = default_timer() - start
        if int(setup_time) > timeout_seconds:
            raise Exception(f"Sandbox setup timed out after {timeout_seconds}")
        if state == "Error":
            print("Sandbox setup failed. Stopping sandbox")
            stop_sandbox(api, sandbox_id, timeout_seconds=timeout_seconds)
            raise Exception("Job Failed during setup")
    print(f"sandbox setup completed after {int(default_timer() - start)} seconds")
    return sandbox_id


def stop_sandbox(api: SandboxRestApiSession, sandbox_id: str, timeout_seconds=1200):
    print("Stopping sandbox and polling teardown...")
    api.stop_sandbox(sandbox_id)
    res = api.get_sandbox_details(sandbox_id)
    state = res["state"]
    start = default_timer()
    while state != "Ended":
        res = api.get_sandbox_details(sandbox_id)
        state = res["state"]
        print(f"Sandbox state: {state}")
        sleep(5)
        teardown_time = default_timer() - start
        if int(teardown_time) > timeout_seconds:
            raise Exception(f"Sandbox teardown timed out after {timeout_seconds}")
    print(f"sandbox teardown completed after {int(default_timer() - start)} seconds")


def run_blocking_command(api: SandboxRestApiSession, dut_component, sandbox_id, command_name: str, timeout_seconds=600):
    print(f'start command on component {dut_component["name"]}')
    res = api.run_component_command(sandbox_id=sandbox_id,
                                    component_id=dut_component["id"],
                                    command_name=command_name,
                                    print_output=True)
    execution_id = res["executionId"]
    execution_details = api.get_execution_details(execution_id)
    execution_status = execution_details["status"]
    start = default_timer()
    print("start polling commmand..")
    while execution_status != "Completed":
        execution_details = api.get_execution_details(execution_id)
        execution_status = execution_details["status"]
        print(f"command status: {execution_status}")
        time.sleep(10)
        execution_time = int(default_timer() - start)
        if execution_time > timeout_seconds:
            raise Exception(f"Command {command_name} timed out after {timeout_seconds} seconds")
    execution_output = execution_details["output"]
    return execution_output


def run_test_logic(api: SandboxRestApiSession, sandbox_id: str, target_model: str):
    print("Starting Test!")

    # pull details and print
    details = api.get_sandbox_details(sandbox_id)
    print("sandbox details:")
    print(json.dumps(details, indent=4))
    components = details["components"]
    print(f"Total components found: {len(components)}")

    # look for dut matching target cloudshell model
    put_search = [x for x in components if x["component_type"] == target_model]
    if not put_search:
        raise Exception("Can't find target DUT")

    # naively take just the first one
    dut_component = put_search[0]

    # run command and poll for output
    output = run_blocking_command(api, dut_component, sandbox_id, command_name="health_check", timeout_seconds=300)
    print(f"command output: '{output}'")

    # that's it for this sample implementation
    print("test complete!")


if __name__ == "__main__":
    TARGET_BLUEPRINT = "sb rest demo"
    TARGET_DUT_MODEL = "Putshell"
    api = SandboxRestApiSession(host="localhost", username="admin", password="admin", domain="Global")

    # start flow
    sb_id = start_sandbox(api, TARGET_BLUEPRINT)
    run_test_logic(api, sb_id, TARGET_DUT_MODEL)
    stop_sandbox(api, sb_id)
