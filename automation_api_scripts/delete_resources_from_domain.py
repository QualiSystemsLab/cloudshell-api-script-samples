from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"

TARGET_DOMAIN = "Global"
domain = TARGET_DOMAIN

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

resource_info = api.GetResourceDetails(resourceFullPath="my Cisco Switch")
pass

api.Attribute

api.UpdatePhysicalConnection(resourceAFullPath='my Cisco Switch/Chassis 0/FastEthernet0-12',
                             resourceBFullPath="Mock_L1/Blade 2/Port 001",
                             overrideExistingConnections=True)