from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

target_resources = api.FindResources(resourceModel="Ftpserver").Resources
my_ftp = target_resources[0]
ftp_details = api.GetResourceDetails(resourceFullPath=my_ftp.Name)
attrs = ftp_details.ResourceAttributes
model = ftp_details.ResourceModelName
target_attr = "{}.Golden Configs Folder".format(model)
golden_configs_val = [attr for attr in attrs if attr.Name == target_attr][0].Value
pass