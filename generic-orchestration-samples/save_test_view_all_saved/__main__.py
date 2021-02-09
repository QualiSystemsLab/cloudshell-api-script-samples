from cloudshell.workflow.orchestration.sandbox import Sandbox
from first_module import first_module_flow

sandbox = Sandbox()
sandbox.execute_save()

# run after save
first_module_flow(sandbox)
