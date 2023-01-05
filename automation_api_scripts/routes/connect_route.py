"""
connect routes one by one with multiple requests
"""
from cloudshell.api.cloudshell_api import CloudShellAPISession


SANDBOX_ID = "ccd3cdb4-da62-442e-8c23-ff9372837d61"
api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")

res_details = api.GetReservationDetails(reservationId=SANDBOX_ID, disableCache=True).ReservationDescription
routes = res_details.RequestedRoutesInfo
print(f"Routes found: {len(routes)}")

for route in routes:
    print(f"Connecting route {route.Source} --> {route.Target}")
    res = api.ConnectRoutesInReservation(reservationId=SANDBOX_ID, endpoints=[route.Source, route.Target], mappingType="bi")

print("done")
