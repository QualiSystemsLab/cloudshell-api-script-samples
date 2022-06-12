from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
from port_from_connector import get_port_from_connector_alias

LIVE_SANDBOX_ID = "87df6742-0fd6-43e4-b068-48764b97d7e5"
TARGET_RESOURCE_NAME = "DUT mock 1"
TARGET_ALIAS = "1"

attach_to_cloudshell_as(user="admin",
                        password="admin",
                        domain="Global",
                        reservation_id=LIVE_SANDBOX_ID,
                        server_address="localhost",
                        resource_name=TARGET_RESOURCE_NAME)

get_port_from_connector_alias(TARGET_ALIAS)
