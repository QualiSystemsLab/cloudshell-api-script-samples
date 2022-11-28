from cloudshell.api.cloudshell_api import CloudShellAPISession

SANDBOX_ID = "6c30767e-c495-4d3a-9a1b-c25a335d8205"

api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
res = api.AddRoutesToReservation(reservationId=SANDBOX_ID,
                                 sourceResourcesFullPath="DUT Mock 2/Port 1",
                                 targetResourcesFullPath="DUT Mock 2/Port 1",
                                 mappingType="bi",
                                 routeAlias="test api")
pass
