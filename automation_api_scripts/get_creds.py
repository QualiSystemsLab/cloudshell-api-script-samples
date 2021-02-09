from cloudshell.api.cloudshell_api import CloudShellAPISession
api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
attrs = api.GetResourceDetails("TP-ASR907-03").ResourceAttributes
pw = [x.Value for x in attrs if x.Name.endswith("Password")]
decrypted = api.DecryptPassword(pw[0]).Value
print(decrypted)