from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
from credentials import credentials
from send_cli_command import send_cli_command_flow

LIVE_SANDBOX_ID = "47f2b606-b335-4918-87e7-0297c06f1c01"
TARGET_RESOURCE_NAME = "mock_6"
TARGET_SERVICE_NAME = None

attach_to_cloudshell_as(user=credentials["user"],
                        password=credentials["password"],
                        domain=credentials["domain"],
                        reservation_id=LIVE_SANDBOX_ID,
                        server_address=credentials['server'],
                        resource_name=TARGET_RESOURCE_NAME,
                        service_name=TARGET_SERVICE_NAME)

send_cli_command_flow()
