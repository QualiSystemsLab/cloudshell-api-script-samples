from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from check_vcenter_cluster import validate_cluster_flow

sandbox = Sandbox()
DefaultSetupWorkflow().register(sandbox)
sandbox.workflow.add_to_preparation(validate_cluster_flow)
sandbox.execute_setup()
