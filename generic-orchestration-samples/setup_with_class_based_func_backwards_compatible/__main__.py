from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from extended_models import CustomSandbox
from blueprint_commands import BlueprintCommands, command_with_sandbox_param, command_with_sandbox_and_components_params

# instantiate custom sandbox object
sandbox = CustomSandbox()

# instantiate class based commands container
bp_commands = BlueprintCommands(sandbox)

# register sandbox with default workflow class
DefaultSetupWorkflow().register(sandbox)

# pass in both custom class based and function based commands
sandbox.workflow.on_configuration_ended(bp_commands.command_one)
sandbox.workflow.on_configuration_ended(command_with_sandbox_param)
sandbox.workflow.on_configuration_ended(command_with_sandbox_and_components_params)

sandbox.execute_setup()
