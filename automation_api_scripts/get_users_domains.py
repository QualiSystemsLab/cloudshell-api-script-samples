from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

SANDDBOX_ID = "37170584-46a5-4634-91aa-54c50e13b552"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

user_details = api.GetUserDetails()
api.Domain
pass


