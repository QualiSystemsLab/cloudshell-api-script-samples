from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from cloudshell.workflow.orchestration.sandbox import Sandbox
from first_module import first_module_flow

sandbox = Sandbox()

# SETUP FLOW BOILERPLATE
DefaultSetupWorkflow().register(sandbox)
sandbox.workflow.on_preparation_ended(first_module_flow, None)
sandbox.execute_setup()
