from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
sandbox_id = "2012cd78-1325-4db8-9dfb-6801e84ea969"
saved_sandbox_name = "test from python"
saved_sandbox_description = "sample description"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

saved_id = api.SaveSandbox(reservationId=sandbox_id,
                      savedSandboxName=saved_sandbox_name,
                      savedSandboxDescription=saved_sandbox_description).SavedSandboxId
print(saved_id)
pass
