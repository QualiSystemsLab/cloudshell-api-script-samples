from cloudshell.helpers.scripts.cloudshell_scripts_helpers import get_reservation_context_details, get_api_session, \
    get_resource_context_details
from cli import SSHHandler
import os

COMMAND_PARAM = "command"
cli_command = os.environ.get(COMMAND_PARAM)
if not cli_command:
    raise ValueError(f"Did not receive cli command param {COMMAND_PARAM}")

api = get_api_session()
sb_details = get_reservation_context_details()
sb_id = sb_details.id

resource_details = get_resource_context_details()
model = resource_details.model
name = resource_details.name
ip = resource_details.address
attrs = resource_details.attributes
normalized_attrs = {k.split(".")[-1]: v for k, v in attrs.items()}

user = normalized_attrs["User"]
if not user:
    raise ValueError("Please populate User attribute for SSH session")
encrypted_password = normalized_attrs["Password"]
decrypted_password = api.DecryptPassword(encrypted_password).Value
if not decrypted_password:
    raise ValueError("Please populate Password attribute for SSH login")

api.WriteMessageToReservationOutput(reservationId=sb_id,
                                    message=f"Sending command to '{name}' at IP: {ip}")

cli = SSHHandler(ip, user, decrypted_password)
output = cli.send_command(cli_command)

# printing to std_out will be the return value of resource scripts
print(output)
