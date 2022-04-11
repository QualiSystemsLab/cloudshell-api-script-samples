from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from configure_apps import configure_sandbox_owner_mail_on_app

sandbox = Sandbox()

DefaultSetupWorkflow().register(sandbox, enable_configuration=False)
sandbox.workflow.add_to_configuration(configure_sandbox_owner_mail_on_app)
sandbox.execute_setup()
