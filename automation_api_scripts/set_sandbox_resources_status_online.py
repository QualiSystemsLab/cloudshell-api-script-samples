from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"

my_resources = ["myAzure", "myVcenter"]

api = CloudShellAPISession(host=server, username=user, password=password, domain="Global")

print("setting Live statuses....")

for resource_name in my_resources:
    api.SetResourceLiveStatus(resourceFullName=resource_name, liveStatusName="Online",
                              additionalInfo="This was set by admin script")

print("Done.")

