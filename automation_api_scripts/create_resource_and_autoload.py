from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"

TARGET_MODEL = "<MY_MODEL>"

api = CloudShellAPISession(host=server, username=user, password=password, domain="Global")

duts = api.FindResources(resourceModel=TARGET_MODEL).Resources