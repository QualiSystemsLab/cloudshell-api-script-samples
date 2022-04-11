from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from cloudshell.workflow.orchestration.sandbox import Sandbox
from dut_health_check import run_dut_health_check

sandbox = Sandbox()

DefaultSetupWorkflow().register(sandbox)
sandbox.workflow.on_configuration_ended(run_dut_health_check, None)
sandbox.execute_setup()
