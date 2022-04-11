from extended_models import CustomSandbox, CustomSetupWorkflow
from blueprint_commands import BlueprintCommands

sandbox = CustomSandbox()

bp_commands = BlueprintCommands(sandbox)

CustomSetupWorkflow(sandbox).register()
sandbox.workflow.on_configuration_ended(bp_commands.command_one)
sandbox.workflow.on_configuration_ended(bp_commands.command_two)
sandbox.execute_setup()
