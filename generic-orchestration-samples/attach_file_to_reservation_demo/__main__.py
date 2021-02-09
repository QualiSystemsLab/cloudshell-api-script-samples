from cloudshell.workflow.orchestration.sandbox import Sandbox
from first_module import run_custom_command
from debug_mode import debug_mode

# ========== Debug helper ==========
if debug_mode:
    from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
    sandbox_id = '109920ef-48fe-4082-b7c2-a6e8203bc444'
    attach_to_cloudshell_as(user='admin',
                            password='admin',
                            domain='Global',
                            reservation_id=sandbox_id,
                            server_address='localhost')

sandbox = Sandbox()
run_custom_command(sandbox=sandbox, components=None)








