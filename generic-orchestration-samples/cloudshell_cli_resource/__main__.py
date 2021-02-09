from cloudshell.workflow.orchestration.sandbox import Sandbox
from first_module import first_module_flow

sandbox = Sandbox()

# FOR BLUEPRINT / RESOURCE LEVEL COMMAND
first_module_flow(sandbox=sandbox, components=None)

# SETUP FLOW BOILERPLATE
"""
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
DefaultSetupWorkflow().register(sandbox)
sandbox.workflow.on_configuration_ended(first_module_flow, None)
sandbox.execute_setup()
"""

# TEARDOWN FLOW BOILERPLATE
"""
from cloudshell.workflow.orchestration.teardown.default_teardown_orchestrator import DefaultTeardownWorkflow
DefaultTeardownWorkflow().register(sandbox)
sandbox.workflow.before_teardown_started(first_module_flow, None)
sandbox.execute_teardown()
"""
