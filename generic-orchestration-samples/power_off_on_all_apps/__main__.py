from cloudshell.workflow.orchestration.sandbox import Sandbox
from first_module import run_custom_command
from debug_mode import debug_mode

# ========== Debug helper ==========
if debug_mode:
    sandbox_id = '5a7fc302-4777-4c6b-9cbe-91133c0feacf'
    cloud_shell_server = '137.117.197.55'
    from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
    attach_to_cloudshell_as(user='admin',
                            password='quali_root',
                            domain='Global',
                            reservation_id=sandbox_id,
                            server_address=cloud_shell_server)

sandbox = Sandbox()
run_custom_command(sandbox=sandbox, components=None)








