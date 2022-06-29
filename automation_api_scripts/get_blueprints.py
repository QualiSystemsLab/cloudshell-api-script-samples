from cloudshell.api.cloudshell_api import CloudShellAPISession

# api session details
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

all_blueprints = api.GetTopologiesByCategory().Topologies

print(f"total blueprints found: {len(all_blueprints)}")
