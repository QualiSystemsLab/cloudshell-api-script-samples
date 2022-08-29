from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
import credentials as creds
from health_check import run_health_check

LIVE_SANDBOX_ID = "bdef5bac-308c-428f-89dd-842e8edec772"
RESOURCE_NAME = "Ubuntu Client_a59a-4547"

attach_to_cloudshell_as(user=creds.USER,
                        password=creds.PASSWORD,
                        domain=creds.DOMAIN,
                        reservation_id=LIVE_SANDBOX_ID,
                        server_address=creds.SERVER,
                        resource_name=RESOURCE_NAME)
run_health_check()