from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.api.cloudshell_api import CloudShellAPISession
import json


sandbox = Sandbox()


def print_sandbox_data_keys(api: CloudShellAPISession, res_id: str):
    data = api.GetSandboxData(res_id)
    api.WriteMessageToReservationOutput(res_id, "=== All Sandbox Keys ===")
    for data in data.SandboxDataKeyValues:

        # pretty print the JSON if valid
        try:
            data_val = json.dumps(json.loads(data.Value), indent=4)
        except Exception:
            data_val = data.Value
        outp = f"sb_data_key: {data.Key}\n{data_val}"

        api.WriteMessageToReservationOutput(res_id, outp)
        api.WriteMessageToReservationOutput(res_id, "=========================")


print_sandbox_data_keys(sandbox.automation_api, sandbox.id)
