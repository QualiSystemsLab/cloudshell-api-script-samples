from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from tenacity import retry, stop_after_attempt, wait_fixed
from cloudshell.helpers.sandbox_reporter.reporter import SandboxReporter

sandbox = Sandbox()

DefaultSetupWorkflow().register(sandbox)
reporter = SandboxReporter(api=sandbox.automation_api,
                           reservation_id=sandbox.id,
                           logger=sandbox.logger)


@retry(stop=(stop_after_attempt(5)), wait=wait_fixed(30))
def execute_setup_with_retries():
    reporter.warning("Beginning setup")
    raise Exception("woops")
    sandbox.execute_setup()


execute_setup_with_retries()
