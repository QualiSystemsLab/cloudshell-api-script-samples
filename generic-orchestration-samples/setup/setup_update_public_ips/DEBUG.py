from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
import credentials
from config_ginger import configure_ginger_agents

LIVE_SANDBOX_ID = "bda46630-f777-401c-a27e-c055f6e6732b"

attach_to_cloudshell_as(user=credentials.USER,
                        password=credentials.PASSWORD,
                        domain=credentials.DOMAIN,
                        reservation_id=LIVE_SANDBOX_ID,
                        server_address=credentials.SERVER)

sandbox = Sandbox()
configure_ginger_agents(sandbox)
pass
