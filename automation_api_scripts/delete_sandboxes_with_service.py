from cloudshell.api.cloudshell_api import CloudShellAPISession
from pprint import pprint
from timeit import default_timer

# set list of service "Alias"
TARGET_SERVICE_MODEL = "Ansible Config 2G"

# api session details
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)


# FIND SANDBOXES
all_sandboxes = api.GetScheduledReservations(fromTime="01/01/2020 00:00",
                                             untilTime="04/02/2021 00:00").Reservations

print("starting operation for {} sandboxes...".format(len(all_sandboxes)))
start = default_timer()
for index, curr_sb in enumerate(all_sandboxes):
    print("checking index: {}".format(index))
    sb_id = curr_sb.Id
    try:
        details = api.GetReservationDetails(sb_id).ReservationDescription
    except Exception as e:
        print("issue getting details for {}".format(sb_id))
        continue

    sb_services = details.Services
    sb_service_names = [service.ServiceName for service in sb_services]
    for sb_service_name in sb_service_names:
        if TARGET_SERVICE_MODEL == sb_service_name:
            try:
                print("deleting: {}".format(sb_id))
                api.DeleteReservation(sb_id)
            except Exception as e:
                print("issue deleting {}".format(sb_id))
                # raise

print("Total time: {}".format(default_timer() - start))
