from cloudshell.api.cloudshell_api import CloudShellAPISession

TARGET_RESOURCES = ["mock_3/Port 4", "my Cisco Switch/Chassis 0/FastEthernet0-6"]

# api session details
user = "admin"
password = "admin"
server = "localhost"

api = CloudShellAPISession(host=server, username=user, password=password, domain="Global")


domain_blueprints = api.GetDomainDetails("Global").Topologies
pass


