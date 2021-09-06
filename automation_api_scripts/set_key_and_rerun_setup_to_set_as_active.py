from cloudshell.api.cloudshell_api import CloudShellAPISession, SandboxDataKeyValue

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

SANDBOX_ID = "b8e1aea9-4d65-43c9-ac0d-227842fe5773"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

api.ExecuteEnvironmentCommand(reservationId=SANDBOX_ID,
                              commandName="Setup")

api
# # SET DATA
# data1 = SandboxDataKeyValue("Key1", "my info 1")
# data2 = SandboxDataKeyValue("Key2", "my info 2")
# data_list = [data1, data2]
# api.SetSandboxData(reservationId=SANDBOX_ID, sandboxDataKeyValues=data_list)
#
# # GET DATA
# sb_data = api.GetSandboxData(SANDBOX_ID).SandboxDataKeyValues
# for item in sb_data:
#     print("Key: {}, Value: {}".format(item.Key, item.Value))



