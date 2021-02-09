from cloudshell.api.cloudshell_api import CloudShellAPISession, ResourceInfoDto

user = "admin"
password = "admin"
server = "localhost"
domain = "Training"
res_id = "775dc625-28a4-4b4d-b07d-58802ca662ca"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)


api.CreateResources()

res = api.AddPermittedUsersToReservation(reservationId=res_id, usernames=["student A"])

pass