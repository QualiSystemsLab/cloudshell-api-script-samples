from cloudshell.workflow.orchestration.teardown.default_teardown_orchestrator import DefaultTeardownWorkflow
from cloudshell.workflow.orchestration.sandbox import Sandbox
from first_module import first_module_flow

sandbox = Sandbox()

DefaultTeardownWorkflow().register(sandbox)
sandbox.workflow.before_teardown_started(first_module_flow, None)
sandbox.execute_teardown()
