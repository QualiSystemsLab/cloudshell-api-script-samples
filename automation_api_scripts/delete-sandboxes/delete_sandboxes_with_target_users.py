from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

from_time = "01/01/2018 00:00"
to_time = "01/01/2022 00:00"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)
all_sandboxes = api.GetScheduledReservations(fromTime=from_time, untilTime=to_time).Reservations

print("Deleting Sandboxes...")
for sandbox in all_sandboxes:
    print("Deleting sandbox '{}'".format(sandbox.Id))
    try:
        api.DeleteReservation(sandbox.Id)
    except Exception as e:
        print("Error deleting sandbox '{}'. Exception - \n{}: {}".format(sandbox.Id, type(e).__name__, str(e)))
        print("===============")

print("Delete sandboxes script done.")
