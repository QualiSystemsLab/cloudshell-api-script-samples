from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

SANDBOX_ID = "b8e1aea9-4d65-43c9-ac0d-227842fe5773"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

sandbox_details = api.GetReservationDetails(reservationId=SANDBOX_ID, disableCache=True).ReservationDescription

print("setting Live statuses on resources in sandbox '{}'....".format(sandbox_details.Name))

for resource in sandbox_details.Resources:
    print("Setting resource '{}'...".format(resource.Name))
    api.SetResourceLiveStatus(resourceFullName=resource.Name,
                              liveStatusName="Online",
                              additionalInfo="Resource is online")

print("Done.")

