from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

users = api.GetAllUsersDetails().Users
print(f"total users in system: {len(users)}")
pass
