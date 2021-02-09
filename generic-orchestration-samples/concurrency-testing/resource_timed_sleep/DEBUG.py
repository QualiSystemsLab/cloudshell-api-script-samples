from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
from credentials import credentials
from first_module import first_module_flow

LIVE_SANDBOX_ID = "1a50d4bf-353e-4d85-9824-7561084a7594"
TARGET_RESOURCE_NAME = "mock_6"
TARGET_SERVICE_NAME = None

attach_to_cloudshell_as(user=credentials["user"],
                        password=credentials["password"],
                        domain=credentials["domain"],
                        reservation_id=LIVE_SANDBOX_ID,
                        server_address=credentials['server'],
                        resource_name=TARGET_RESOURCE_NAME,
                        service_name=TARGET_SERVICE_NAME)

first_module_flow()
