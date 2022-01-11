from cloudshell.api.cloudshell_api import CloudShellAPISession

# start session
api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")

# find resources in DB - specify models / family / attributes etc
all_resources = api.FindResources(resourceModel="Putshell").Resources
print(f"resource count found: {len(all_resources)}")
