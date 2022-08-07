from cloudshell.workflow.orchestration.setup.default_setup_orchestrator import DefaultSetupWorkflow
from cloudshell.workflow.orchestration.sandbox import Sandbox
from replace_quali_server import replace_quali_server_app
from config_linux import configure_linux_es

sandbox = Sandbox()

replace_quali_server_app(sandbox)

DefaultSetupWorkflow().register(sandbox, enable_configuration=False)
sandbox.workflow.add_to_configuration(configure_linux_es)
sandbox.execute_setup()
