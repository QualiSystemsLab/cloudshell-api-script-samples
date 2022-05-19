from cloudshell.cli.service.cli import CLI
from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.cli.service.command_mode import CommandMode


class SSHHandler:
    def __init__(self, ip, user, password, prompt="#"):
        self.cli = CLI()
        self.mode = CommandMode(prompt)
        self.session_types = [SSHSession(host=ip, username=user, password=password)]

    def send_command(self, command):
        with self.cli.get_session(self.session_types, self.mode) as cli_service:
            output = cli_service.send_command(command)
        return output
