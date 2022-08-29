from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
import credentials as creds
from configure_apps import custom_configure_apps

LIVE_SANDBOX_ID = "bdef5bac-308c-428f-89dd-842e8edec772"

attach_to_cloudshell_as(user=creds.USER,
                        password=creds.PASSWORD,
                        domain=creds.DOMAIN,
                        reservation_id=LIVE_SANDBOX_ID,
                        server_address=creds.SERVER)

sandbox = Sandbox()
custom_configure_apps(sandbox)