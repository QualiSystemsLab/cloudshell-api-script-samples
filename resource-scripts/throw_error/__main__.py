from cloudshell.helpers.scripts.cloudshell_scripts_helpers import get_reservation_context_details, get_api_session, \
    get_resource_context_details

api = get_api_session()
sb_details = get_reservation_context_details()
sb_id = sb_details.id

resource_details = get_resource_context_details()
name = resource_details.name
ip = resource_details.address

api.WriteMessageToReservationOutput(reservationId=sb_id,
                                    message=f"Resource name: {name}, IP: {ip}")

raise Exception(f"Resource {name} exploded during operation!!!")
