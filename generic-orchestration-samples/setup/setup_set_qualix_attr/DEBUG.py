from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
from credentials import credentials
from sandbox_commands import first_module_flow

LIVE_SANDBOX_ID = "b2f196a5-b0f3-47d7-9c38-66d24ff98bbc"

attach_to_cloudshell_as(user=credentials["user"],
                        password=credentials["password"],
                        domain=credentials["domain"],
                        reservation_id=LIVE_SANDBOX_ID,
                        server_address=credentials['server'])

sandbox = Sandbox()
first_module_flow(sandbox=sandbox, components=None)
