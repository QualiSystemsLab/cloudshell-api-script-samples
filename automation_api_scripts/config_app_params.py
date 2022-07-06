from cloudshell.api.cloudshell_api import CloudShellAPISession, AppConfiguration, ConfigParam

session = CloudShellAPISession("localhost", "admin", "admin", "Global")
res_id = "260b3f80-14bd-4cc2-975c-6ab21a12ac28"

res_details = session.GetReservationDetails(res_id).ReservationDescription
x = session.GetAppsDetailsInReservation(res_id, ["Linux Ubuntu Tiny"])
params = [ConfigParam("key", "value")]
app_configs = [AppConfiguration(AppName="asdf", ConfigParams=params)]

session.ConfigureApps(reservationId=res_id,
                      appConfigurations=app_configs)

res_details_after_config = session.GetReservationDetails(res_id).ReservationDescription
