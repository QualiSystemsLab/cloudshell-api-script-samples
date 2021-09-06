from cloudshell.api.cloudshell_api import CloudShellAPISession, UpdateTopologyGlobalInputsRequest

# cloudshel credentials
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

TARGET_BLUEPRINT = "qualix tag dev"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

global_inputs = [UpdateTopologyGlobalInputsRequest(ParamName="My Input", Value="whatever")]

try:
    response = api.CreateImmediateTopologyReservation(reservationName="test sandbox",
                                                      owner="admin",
                                                      durationInMinutes=60,
                                                      notifyOnStart=True,
                                                      notifyOnEnd=True,
                                                      notificationMinutesBeforeEnd=10,
                                                      topologyFullPath=TARGET_BLUEPRINT,
                                                      globalInputs=global_inputs,
                                                      notifyOnSetupComplete=True).Reservation
except Exception as e:
    exc_msg = "'{}' blueprint start failed.\n{}: {}".format(TARGET_BLUEPRINT, type(e).__name__, str(e))
    raise Exception(exc_msg)

print("Sandbox {} started".format(response.Id))


