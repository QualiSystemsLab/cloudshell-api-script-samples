import cloudshell.api.cloudshell_api as api

# username = 'admin'
# password = 'admin'
# server = 'localhost'
# domain = 'Global'

username = 'admin'
password = 'civ1C2018'
server = '172.30.180.86'
domain = 'Global'

session = api.CloudShellAPISession(
    username=username,
    password=password,
    domain=domain,
    host=server
)

all_cs_users = session.GetAllUsersDetails().Users
print(len(all_cs_users))
