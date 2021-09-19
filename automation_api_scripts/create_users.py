from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

USER_COUNT = 5

# print("adding users...")
# for i in range(USER_COUNT):
#     api.AddNewUser(username="{}-user".format(i+1),
#                    password="1111",
#                    email="test@test.com",
#                    isActive=True)

print("deleting users...")
for i in range(USER_COUNT):
    api.DeleteUser(username="{}-user".format(i+1))

print("done")
