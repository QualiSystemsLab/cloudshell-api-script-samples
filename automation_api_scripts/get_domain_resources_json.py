from cloudshell.api.cloudshell_api import CloudShellAPISession
import json

# add credentials for session
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

# select target domain
TARGET_DOMAIN = "MC"


# start session
api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

# find resources of target model
domain_details = api.GetDomainDetails(domainName=TARGET_DOMAIN)
resources = domain_details.Resources

resources_json = json.dumps(resources, default=lambda x: x.__dict__)
print(resources_json)
