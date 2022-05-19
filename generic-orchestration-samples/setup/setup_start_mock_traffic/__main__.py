from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from cloudshell.workflow.orchestration.sandbox import Sandbox
from start_traffic import start_traffic_flow
from dut_health_check import run_dut_health_check

sandbox = Sandbox()

DefaultSetupWorkflow().register(sandbox)
sandbox.workflow.on_connectivity_ended(run_dut_health_check)
sandbox.workflow.on_configuration_ended(start_traffic_flow)
sandbox.execute_setup()
