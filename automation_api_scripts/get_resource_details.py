from cloudshell.api.cloudshell_api import CloudShellAPISession

# add credentials
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

# start session
api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)


app = 'mock_1'
# find resources of target model
res_details = api.GetResourceDetails(resourceFullPath=app)
x = api.GetResourceAvailability([app])
pass