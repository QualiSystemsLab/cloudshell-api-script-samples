from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"

session = CloudShellAPISession(host=server, username=user, password=password, domain="Global")

res = session.UpdatePhysicalConnection(resourceAFullPath="celare dummy 2/Chassis 1/Module 1/Port 10",
                                       resourceBFullPath="L1Mock1/Blade 1/Port 003",
                                       overrideExistingConnections=True)