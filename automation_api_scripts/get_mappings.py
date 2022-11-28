import time

from cloudshell.api.cloudshell_api import CloudShellAPISession

# TARGET_RESOURCE = "L1Mock1"
TARGET_RESOURCE = "DUT Mock 2"
api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
res = api.GetResourceMappings(resources=[TARGET_RESOURCE])
# res = api.MapPorts(sourcePort="L1Mock1/Blade 1/Port 004",
#                    destinationPort="L1Mock1/Blade 1/Port 004",
#                    mappingType="bi")
pass