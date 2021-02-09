from cloudshell.api.cloudshell_api import CloudShellAPISession
import timeit

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

TARGET_RESOURCE_NAME = "tent-switch-test"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

print("starting autoload...")
start_time = timeit.default_timer()
res = api.AutoLoad(resourceFullPath=TARGET_RESOURCE_NAME)
elapsed = timeit.default_timer() - start_time

print("autoload response: {}".format(res))
print("autoload time: {}".format(elapsed))