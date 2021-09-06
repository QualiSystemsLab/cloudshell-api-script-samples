from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

RESOURCE_NAME = "mock1"
TARGET_IP = "192.168.5.1"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

print("Setting resource '{}' to IP '{}'".format(RESOURCE_NAME, TARGET_IP))

api.UpdateResourceAddress(resourceFullPath=RESOURCE_NAME,
                          resourceAddress=TARGET_IP)

print("done.")