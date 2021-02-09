from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"

session = CloudShellAPISession(host=server, username=user, password=password, domain="Global")

res = session.UpdatePhysicalConnection(resourceAFullPath="my Cisco Switch/Chassis 0/FastEthernet0-10",
                                       resourceBFullPath="Mock_L1/Blade 1/Port 001",
                                       overrideExistingConnections=True)