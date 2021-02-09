from cloudshell.api.cloudshell_api import CloudShellAPISession

# api session details
user = "admin"
password = "admin"
server = "localhost"

api = CloudShellAPISession(host=server, username=user, password=password, domain="Global")

sandboxes = api.GetScheduledReservations(fromTime="01/22/2020 00:00", untilTime="01/23/2020 16:00").Reservations
filter = [sb for sb in sandboxes if sb.Name=="MC Test"]
details = api.GetReservationDetails(reservationId=filter[0].Id)

first_reservation_details = api.GetReservationDetails(reservationId=sandboxes[0].Id)
pass

