from cloudshell.api.cloudshell_api import InputNameValue, SandboxDataKeyValue, CloudShellAPISession


user = "admin"
password = "admin"
server = "localhost"

api = CloudShellAPISession(host=server, username=user, password=password, domain="Global")

res_id = "64aaa89b-46e4-4df1-8ff5-b789109f1cf1"

# reset sandbox data
api.ClearSandboxData(res_id)

# save sandbox data
all_sb_data = []
sb_timestamp_data = SandboxDataKeyValue('key with spaces', "lmao bitchhh")
all_sb_data.append(sb_timestamp_data)
api.SetSandboxData(res_id, all_sb_data)

