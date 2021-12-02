import json
from collections import OrderedDict
from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

# Get all active sandboxes
active_sandboxes = api.GetCurrentReservations().Reservations

if not active_sandboxes:
    print("No currently active sandboxes")
    exit(0)

print("Active sandboxes")
for sandbox in active_sandboxes:
    target_keys = [
        ("id", sandbox.Id),
        ("name", sandbox.Name),
        ("owner", sandbox.Owner),
        ("status", sandbox.Status),
        ("start_time", sandbox.StartTime),
        ("end_time", sandbox.EndTime),
        ("source_blueprint", sandbox.Topologies[0]),
    ]
    curr_dict = OrderedDict(target_keys)
    print(json.dumps(curr_dict, indent=4))
