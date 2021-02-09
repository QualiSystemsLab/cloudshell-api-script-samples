from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from cloudshell.workflow.orchestration.setup.vbp.configuration_commands import configure_virtual_chassis
from cloudshell.workflow.orchestration.sandbox import Sandbox

sandbox = Sandbox()

# SETUP FLOW BOILERPLATE
DefaultSetupWorkflow().register(sandbox)
sandbox.workflow.on_configuration_ended(configure_virtual_chassis, sandbox.components.apps)
sandbox.execute_setup()
