from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"

session = CloudShellAPISession(host=server, username=user, password=password, domain="Global")

response = session.MapPorts(sourcePort="Mock_L1/Blade 2/Port 002",
                            destinationPort="Mock_L1/Blade 2/Port 003",
                            mappingType="bi")

