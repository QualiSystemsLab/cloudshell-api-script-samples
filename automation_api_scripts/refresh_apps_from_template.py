from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

SANDBOX_ID = "3bac3765-ba86-4ad3-819b-3a2127c1cbef"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

api