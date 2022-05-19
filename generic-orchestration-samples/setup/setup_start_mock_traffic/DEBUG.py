from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
import credentials
from dut_health_check import run_dut_health_check
from start_traffic import start_traffic_flow

LIVE_SANDBOX_ID = "4f1c7f14-5e28-4a54-a611-5883ea84b39b"

attach_to_cloudshell_as(user=credentials.USER,
                        password=credentials.PASSWORD,
                        domain=credentials.DOMAIN,
                        reservation_id=LIVE_SANDBOX_ID,
                        server_address=credentials.SERVER)

sandbox = Sandbox()
run_dut_health_check(sandbox=sandbox, components=None)
start_traffic_flow(sandbox)
