from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
from credentials import credentials
from replace_quali_server import register_es_flow

LIVE_SANDBOX_ID = "fdb482fb-6551-4f2a-9fcf-c8b93942120e"
TARGET_RESOURCE_NAME = None
TARGET_SERVICE_NAME = None

attach_to_cloudshell_as(user=credentials["user"],
                        password=credentials["password"],
                        domain=credentials["domain"],
                        reservation_id=LIVE_SANDBOX_ID,
                        server_address=credentials['server'],
                        resource_name=TARGET_RESOURCE_NAME,
                        service_name=TARGET_SERVICE_NAME)

sandbox = Sandbox()
register_es_flow(sandbox)
pass
