from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

SANDBOX_ID = "fbdd8ce6-d68f-424c-a520-234547a07f2c"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

sandbox_details = api.GetReservationDetails(reservationId=SANDBOX_ID, disableCache=True).ReservationDescription

print("setting sandbox stage to end in sandbox '{}'....".format(sandbox_details.Name))

api.SetSetupStage(setupStage="Ended", reservationId=SANDBOX_ID)

print("Done.")

