from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"

TARGET_DOMAIN = "end_users"
domain = TARGET_DOMAIN

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

target_resources = api.FindResources(resourceModel="Putshell").Resources

# get a list of names of target resources
target_resource_names = [resource.Name for resource in target_resources]

res = api.RemoveResourcesFromDomain(domainName=TARGET_DOMAIN, resourcesNames=target_resource_names)
pass
