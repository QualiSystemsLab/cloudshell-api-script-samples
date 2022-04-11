from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from edit_apps import edit_apps_in_sandbox

sandbox = Sandbox()

DefaultSetupWorkflow().register(sandbox)
sandbox.workflow.add_to_preparation(edit_apps_in_sandbox)

sandbox.execute_setup()
