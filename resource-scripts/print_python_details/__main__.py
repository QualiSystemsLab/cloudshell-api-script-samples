from cloudshell.helpers.scripts.cloudshell_scripts_helpers import get_reservation_context_details, get_api_session, \
    get_resource_context_details
import sys
import struct

api = get_api_session()
sb_details = get_reservation_context_details()
sb_id = sb_details.id
resource_details = get_resource_context_details()
name = resource_details.name

api.WriteMessageToReservationOutput(reservationId=sb_id, message=f"script for '{name}' querying interpreter data...")

py_version = sys.version
bit_version = struct.calcsize("P") * 8
interpreter_path = sys.executable


# printing to std_out will be the return value of resource scripts
print(f"python version: {py_version}, bit version: {bit_version}, interpreter path: {interpreter_path}")
