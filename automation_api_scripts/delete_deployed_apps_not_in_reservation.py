"""
Find all apps in "Deployed Apps" Folder and delete resource if not currently in Reservation
This script currently supports V-CENTER cloud provider
Script must have direct connectivity to:
- Quali Application Server
- vCenter Server
"""
from cloudshell.api.cloudshell_api import CloudShellAPISession
import time

CS_USER = "admin"
CS_PASSWORD = "admin"
CS_SERVER = "localhost"
TARGET_APP_FAMILY = "Generic App Family"

api = CloudShellAPISession(host=CS_SERVER, username=CS_USER, password=CS_PASSWORD, domain="Global")
all_app_resources = api.FindResources(resourceFamily=TARGET_APP_FAMILY).Resources
deployed_app_folder_resources = [resource for resource in all_app_resources
                                 if "Deployed Apps" in resource.FullPath]
if not deployed_app_folder_resources:
    print("No deployed app resources. Ending Script.")
    exit(0)

un_reserved_deployed_apps = [resource for resource in deployed_app_folder_resources
                             if resource.ReservedStatus == "Not In Reservations"]

if not un_reserved_deployed_apps:
    print("No UNRESERVED deployed app resources. Ending Script.")
    exit(0)

failed_deletions = []
successful_deletions = []
for resource in un_reserved_deployed_apps:
    try:
        print("Deleting deployed app resource: '{}'...".format(resource.Name))
        response = api.DeleteResource(resourceFullPath=resource.Name)
        response = str(response)
    except Exception as e:
        print("FAILED deletion '{}': Exception: {}".format(resource.Name, str(e)))
        print("=============")
        failed_deletions.append(resource.Name)
    else:
        if 'Success="true"' in response:
            print("SUCCESSFUL deletion: '{}'".format(resource.Name))
            print("=============")
            successful_deletions.append(resource.Name)
        else:
            print("FAILED deletion '{}'. Response: {}".format(resource.Name, response))
            print("=============")
            failed_deletions.append(resource.Name)

if failed_deletions:
    if successful_deletions:
        print("Following apps deleted SUCCESSFULLY: {}".format(successful_deletions))
    print("Following app resource deletion FAILED: {}".format(failed_deletions))
    print("=============")
    time.sleep(1)  # just so exception appears after print statements
    raise Exception("There were failed app resource deletions in this operation.")

print("ALL Un-reserved deployed apps deleted SUCCESSFULLY: {}".format(successful_deletions))
print("=============")
