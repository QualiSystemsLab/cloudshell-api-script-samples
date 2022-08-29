import time

from cloudshell.helpers.scripts.cloudshell_scripts_helpers import get_reservation_context_details, get_api_session, \
    get_resource_context_details
from cli_handler import LinuxSSH


def run_health_check():
    api = get_api_session()
    sb_details = get_reservation_context_details()
    sb_id = sb_details.id

    resource_details = get_resource_context_details()
    name = resource_details.name
    ip = resource_details.address
    attrs = resource_details.attributes
    user = attrs.get("User")
    if not user:
        raise ValueError("User attr not populated")
    encrypted = attrs.get("Password")
    decrypted = api.DecryptPassword(encrypted).Value
    if not decrypted:
        raise ValueError("Password is not defined")
    ssh = LinuxSSH(address=ip, username=user, password=decrypted)
    host_name = ssh.send_command("hostname").splitlines()[0]

    api.WriteMessageToReservationOutput(sb_id, f"Health checking {host_name}...")
    time.sleep(15)
    # printing to std_out will be the return value of resource scripts
    print(f"health check completed for '{name}'")
