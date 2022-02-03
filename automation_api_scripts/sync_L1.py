from cloudshell.api.cloudshell_api import CloudShellAPISession

api = CloudShellAPISession(host="localhost",
                           username="admin",
                           password="admin",
                           domain="Global")

RESOURCE_NAME = "<MY_RESOURCE"

# the raw api calls
sync_from_response = api.SyncResourceFromDevice(resourceFullPath=RESOURCE_NAME)
sync_to_response = api.SyncResourceToDevice(resourceFullPath=RESOURCE_NAME)

# to sync child resources, use get resource details, then iterate over desired resources
root_resource_details = api.GetResourceDetails(RESOURCE_NAME)
child_resources = root_resource_details.ChildResources

for resource in child_resources:
    print("syncing resource {}".format(resource.Name))
    api.SyncResourceFromDevice(resource.Name)

print("done")