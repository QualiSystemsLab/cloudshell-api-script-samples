from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"

api = CloudShellAPISession(host=server, username=user, password=password, domain="Training")

res = api.CreateImmediateReservation(reservationName="lolol",
                                     owner="end_user",
                                     durationInMinutes=60)
res_id = res.Reservation.Id
res = api.AddPermittedUsersToReservation(reservationId=res_id,
                                         usernames=["Student A"])
pass