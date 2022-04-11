from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from cloudshell.workflow.orchestration.sandbox import Sandbox
from sandbox_commands import SandboxCommands
from helper_code.sandbox_reporter import SandboxReporter

sandbox = Sandbox()
reporter = SandboxReporter(api=sandbox.automation_api,
                           reservation_id=sandbox.id,
                           logger=sandbox.logger)

sandbox_commands = SandboxCommands(reporter=reporter)

DefaultSetupWorkflow().register(sandbox)

# CONNECTIVITY
sandbox.workflow.add_to_connectivity(sandbox_commands.set_requested_static_ip, None)

# AFTER CONFIGURATION
sandbox.workflow.on_configuration_ended(sandbox_commands.set_qualix_addresses, None)
sandbox.execute_setup()
