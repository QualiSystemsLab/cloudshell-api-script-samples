from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

res_id = "3bac3765-ba86-4ad3-819b-3a2127c1cbef"
blueprint_name = "L1 connectivity - 9.2 Ogura Test"

res = api.ActivateTopology(reservationId=res_id, topologyFullPath=blueprint_name)
pass