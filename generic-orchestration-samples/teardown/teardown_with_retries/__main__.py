from cloudshell.workflow.orchestration.sandbox import Sandbox
from cloudshell.workflow.orchestration.teardown.default_teardown_orchestrator import DefaultTeardownWorkflow
from tenacity import retry, stop_after_attempt, wait_fixed
from cloudshell.helpers.sandbox_reporter.reporter import SandboxReporter

sandbox = Sandbox()

DefaultTeardownWorkflow().register(sandbox)
reporter = SandboxReporter(api=sandbox.automation_api,
                           reservation_id=sandbox.id,
                           logger=sandbox.logger)


@retry(stop=(stop_after_attempt(5)), wait=wait_fixed(30))
def execute_teardown_with_retries():
    reporter.warning("Beginning teardown")
    raise Exception("woops")
    sandbox.execute_teardown()


execute_teardown_with_retries()
