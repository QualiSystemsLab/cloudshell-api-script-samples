from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from cloudshell.workflow.orchestration.sandbox import Sandbox
from set_public_ips import set_public_ip_flow

sandbox = Sandbox()

DefaultSetupWorkflow().register(sandbox)
sandbox.workflow.on_connectivity_ended(set_public_ip_flow)
sandbox.execute_setup()
