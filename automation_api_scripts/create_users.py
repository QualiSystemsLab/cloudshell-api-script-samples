from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

TOTAL_RESOURCES = 1000

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

print("building resources...")
for i in range(TOTAL_RESOURCES):
    print("resource" + str(i + 1))
    api.CreateResource(resourceModel="Generic Dut",
                       resourceName="generic_dummy_b_{}".format(str(i + 1)),
                       resourceAddress="{0}.{0}.{0}.{0}".format(str(i)),
                       folderFullPath="dummy resources 2")

print("done")
