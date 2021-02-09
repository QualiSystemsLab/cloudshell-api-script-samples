from cloudshell.workflow.orchestration.sandbox import Sandbox
from first_module import first_module_flow

sandbox = Sandbox()

# FOR BLUEPRINT / RESOURCE LEVEL COMMAND
first_module_flow(sandbox=sandbox, components=None)


