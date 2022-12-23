from cloudshell.api.cloudshell_api import CloudShellAPISession

RESERVED_STATUS = "Reserved"

TARGET_RESOURCE = "DUT Mock 2"
api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
available = api.GetResourceAvailability(resourcesNames=[TARGET_RESOURCE]).Resources
pass