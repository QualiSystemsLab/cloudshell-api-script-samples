from cloudshell.workflow.orchestration.sandbox import Sandbox
from custom_setup_workflow import CustomSetupWorkflow

sandbox = Sandbox()

CustomSetupWorkflow().register(sandbox)

sandbox.execute_setup()
