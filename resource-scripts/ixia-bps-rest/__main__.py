from cloudshell.helpers.scripts.cloudshell_scripts_helpers import get_reservation_context_details, get_api_session, \
    get_resource_context_details
from purge_ixia_db import purge_ixia_db_flow

# get resource details from context
api = get_api_session()
sb_details = get_reservation_context_details()
sb_id = sb_details.id
resource_details = get_resource_context_details()

# put interesting data into variables
model = resource_details.model
name = resource_details.name
ip = resource_details.address

# extract data from attributes
attrs = resource_details.attributes
user = attrs[f"{model}.User"]
encrypted_password = attrs[f"{model}.Password"]

# stored password needs to be decrypted
decrypted_password = api.DecryptPassword(encryptedString=encrypted_password).Value

# start flow
api.WriteMessageToReservationOutput(reservationId=sb_id,
                                    message=f"starting purge flow")

purge_ixia_db_flow(ip, user, decrypted_password)

# printing to std_out will be the return value of resource scripts
print(f"Ixia Purge DB flow completed for '{name}'")