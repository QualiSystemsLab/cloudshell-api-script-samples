from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from cloudshell.workflow.orchestration.sandbox import Sandbox
from send_command import send_command

sandbox = Sandbox()

DefaultSetupWorkflow().register(sandbox)
sandbox.workflow.on_configuration_ended(send_command, None)
sandbox.execute_setup()
