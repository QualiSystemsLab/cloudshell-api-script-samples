from cloudshell.cli.service.cli import CLI
from cloudshell.cli.service.session_pool_context_manager import SessionPoolContextManager
from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.cli.service.command_mode import CommandMode


class SSHClientHandler:
    def __init__(self, ip, user, password, prompt="#"):
        self.cli = CLI()
        self.mode = CommandMode(prompt)
        self.session_types = [SSHSession(host=ip, username=user, password=password)]

    @property
    def cli_service(self) -> SessionPoolContextManager:
        return self.cli.get_session(self.session_types, self.mode)

    def send_command(self, command, action_map=None):
        with self.cli_service as cli_service:
            output = cli_service.send_command(command, action_map=action_map)

        return output
