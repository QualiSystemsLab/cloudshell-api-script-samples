from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from first_module import run_custom_command
from debug_mode import debug_mode

# ========== Debug helper ==========
if debug_mode:
    sandbox_id = 'bb963af0-34ad-4cc2-8ad3-eb9f55d8480a'
    cloud_shell_server = 'localhost'
    from cloudshell.helpers.scripts.cloudshell_dev_helpers import attach_to_cloudshell_as
    attach_to_cloudshell_as(user='admin',
                            password='admin',
                            domain='Global',
                            reservation_id=sandbox_id,
                            server_address=cloud_shell_server)

sandbox = Sandbox()

# Manual function call for debugging against live sandbox
if debug_mode:
    run_custom_command(sandbox=sandbox, components=None)

# ========== SETUP WORKFLOW ==========
if not debug_mode:
    DefaultSetupWorkflow().register(sandbox)
    sandbox.workflow.on_preparation_ended(run_custom_command, None)
    sandbox.execute_setup()







