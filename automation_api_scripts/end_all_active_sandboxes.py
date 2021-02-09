from time import sleep

from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

TERMINATE_TEARDOWN = True

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

# Get all active sandboxes
active_sandboxes = api.GetCurrentReservations().Reservations

if not active_sandboxes:
    print("No currently active sandboxes")
    exit(0)

print("===== ending reservations... =====")
for sandbox in active_sandboxes:
    print(sandbox.Name)
    api.EndReservation(reservationId=sandbox.Id)



if TERMINATE_TEARDOWN:
    print("===== terminating teardowns... =====")
    sleep(10)
    for sandbox in active_sandboxes:
        if "teardown" in sandbox.Status.lower():
            print(sandbox.Name)
            api.TerminateReservation(sandbox.Id)