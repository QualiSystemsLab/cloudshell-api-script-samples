from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from configure_apps import custom_configure_apps

sandbox = Sandbox()

DefaultSetupWorkflow().register(sandbox, enable_configuration=False)
sandbox.workflow.add_to_configuration(custom_configure_apps)
sandbox.execute_setup()
