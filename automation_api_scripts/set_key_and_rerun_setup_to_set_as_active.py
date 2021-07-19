from cloudshell.api.cloudshell_api import CloudShellAPISession, SandboxDataKeyValue

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

SANDBOX_ID = "bf3e93a5-5221-4f7d-acac-cf6876f17fe5"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

# SET DATA
data1 = SandboxDataKeyValue("Key1", "my info 1")
data2 = SandboxDataKeyValue("Key2", "my info 2")
data_list = [data1, data2]
api.SetSandboxData(reservationId=SANDBOX_ID, sandboxDataKeyValues=data_list)

# GET DATA
sb_data = api.GetSandboxData(SANDBOX_ID).SandboxDataKeyValues
for item in sb_data:
    print("Key: {}, Value: {}".format(item.Key, item.Value))



