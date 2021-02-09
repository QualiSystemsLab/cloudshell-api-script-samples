"""
Set SCRIPT_FLOW: ["default", "setup", "teardown"]
"""
from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.custom_helpers import sb_print
from helper_code.utility import html_err_wrap
from first_module import first_module_flow

SCRIPT_FLOW = "default"

sandbox = Sandbox()

if SCRIPT_FLOW == "default":
    first_module_flow(sandbox=sandbox, components=None)

elif SCRIPT_FLOW == "setup":
    from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
    DefaultSetupWorkflow().register(sandbox)
    sandbox.workflow.on_configuration_ended(first_module_flow, None)
    sandbox.execute_setup()

elif SCRIPT_FLOW == "teardown":
    from cloudshell.workflow.orchestration.teardown.default_teardown_orchestrator import DefaultTeardownWorkflow
    DefaultTeardownWorkflow().register(sandbox)
    sandbox.workflow.before_teardown_started(first_module_flow, None)
    sandbox.execute_teardown()

else:
    # If SCRIPT_FLOW string set incorrectly
    sb_print(sandbox, html_err_wrap("Please set a correct SCRIPT_FLOW in control_flow.py") +
             "\n" + "choose from: ['default', 'setup', 'teardown']")
    raise Exception('incorrect SCRIPT_FLOW variable set in __main__.py')
