from cloudshell.api.cloudshell_api import CloudShellAPISession

# add credentials
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

# start session
api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

# find resources of target model
saved_sbs = api.GetSavedSandboxes()
pass