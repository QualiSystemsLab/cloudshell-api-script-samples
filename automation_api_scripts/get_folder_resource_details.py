"""
iterate over a target folder and print out reserved resources
"""
from cloudshell.api.cloudshell_api import CloudShellAPISession
from timeit import default_timer

# add credentials for session
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

TARGET_FOLDER = "mocks/DUT"

start = default_timer()

# start session
api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)
# resources = api.GetFolderContent(fullPath="mocks/DUT", showAllDomains=True)

print(f"looking for resource availablity in target folder: {TARGET_FOLDER}")
print("=================")
contents = api.GetFolderContent(fullPath=TARGET_FOLDER).ContentArray


for content in contents:
    if content.Type == "Resource":
        root_resource_name = content.Name
        print(f"root name: {root_resource_name}")
        reserved_resource = {root_resource_name: []}
        availability_resources = api.GetResourceAvailability(resourcesNames=[content.Name]).Resources
        for resource in availability_resources:
            print(f"Resource: {resource.FullName}, Status: {resource.ReservedStatus}")
        print("===========")

print(f"Script done after {default_timer() - start} seconds")