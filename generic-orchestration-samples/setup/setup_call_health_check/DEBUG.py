from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
from credentials import credentials
from dut_health_check import run_dut_health_check

LIVE_SANDBOX_ID = "61f73082-ab61-49b5-98e9-bdcd6f4c290e"

attach_to_cloudshell_as(user=credentials["user"],
                        password=credentials["password"],
                        domain=credentials["domain"],
                        reservation_id=LIVE_SANDBOX_ID,
                        server_address=credentials['server'])

sandbox = Sandbox()
run_dut_health_check(sandbox=sandbox, components=None)
