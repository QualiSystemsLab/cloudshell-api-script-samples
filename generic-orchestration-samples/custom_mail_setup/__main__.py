"""
See control_flow.py to set DEBUG_MODE and SCRIPT_TYPE constants
"""
from control_flow import DEBUG_MODE, SCRIPT_TYPE, LIVE_SANDBOX_ID, TARGET_RESOURCE_NAME, TARGET_SERVICE_NAME
from dev_tools.dev_utility import attach_to_cs_wrapper, get_sandbox_wrapper
from helper_code.custom_helpers import sb_print
from helper_code.helper_utility import html_red
from first_module import first_module_flow

if DEBUG_MODE:
    attach_to_cs_wrapper(LIVE_SANDBOX_ID, TARGET_RESOURCE_NAME, TARGET_SERVICE_NAME)
    sandbox = get_sandbox_wrapper()
    sb_print(sandbox, "=== attached to sandbox in debug mode ===")
    first_module_flow(sandbox=sandbox, components=None)
    exit(0)

# ========== PRODUCTION WORKFLOW ==========
sandbox = get_sandbox_wrapper()

if SCRIPT_TYPE in ["default", "resource", "service"]:
    first_module_flow(sandbox=sandbox, components=None)

elif SCRIPT_TYPE == "setup":
    from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
    DefaultSetupWorkflow().register(sandbox)
    sandbox.workflow.on_configuration_ended(first_module_flow, None)
    sandbox.execute_setup()

elif SCRIPT_TYPE == "teardown":
    from cloudshell.workflow.orchestration.teardown.default_teardown_orchestrator import DefaultTeardownWorkflow
    DefaultTeardownWorkflow().register(sandbox)
    sandbox.workflow.before_teardown_started(first_module_flow, None)
    sandbox.execute_teardown()

else:
    # If SCRIPT_TYPE string set incorrectly in control_flow.py
    sb_print(sandbox, html_red("Please set a correct SCRIPT_TYPE in control_flow.py") +
             "\n" + "choose from: ['setup', 'teardown', 'default', 'resource', 'service']")
    raise Exception('incorrect SCRIPT_TYPE set in control_flow.py of script template')










