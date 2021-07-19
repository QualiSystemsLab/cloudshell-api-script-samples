from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "192.168.85.25"
domain = "Global"

MY_SERVICE = "Ansible Config 2G"
from_time = "12/01/2020 08:00"
to_time = "01/08/2021 16:00"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

all_sandboxes = api.GetScheduledReservations(fromTime=from_time, untilTime=to_time)

print("Deleting Sandboxes...")
for sandbox in all_sandboxes.Reservations:
    api.DeleteReservation(sandbox.Id)

print("Done")