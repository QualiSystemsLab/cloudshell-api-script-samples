from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.api.cloudshell_api import CloudShellAPISession
import json


sandbox = Sandbox()


def print_sandbox_data_keys(api: CloudShellAPISession, res_id: str):
    sandbox_data_key_values = api.GetSandboxData(res_id).SandboxDataKeyValues
    if not sandbox_data_key_values:
        api.WriteMessageToReservationOutput(res_id, "No Sandbox Data found")
        return

    api.WriteMessageToReservationOutput(res_id, "=== All Sandbox Keys ===")
    for data in sandbox_data_key_values:

        # pretty print the JSON if valid
        try:
            data_val = json.dumps(json.loads(data.Value), indent=4)
        except Exception:
            data_val = data.Value
        outp = f"sb_data_key: {data.Key}\n{data_val}"

        api.WriteMessageToReservationOutput(res_id, outp)
        api.WriteMessageToReservationOutput(res_id, "=========================")


print_sandbox_data_keys(sandbox.automation_api, sandbox.id)
