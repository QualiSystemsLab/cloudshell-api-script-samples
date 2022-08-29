from typing import List

from cloudshell.cli.service.cli import CLI
from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.cli.service.command_mode import CommandMode
import time


class LinuxSSH:
    def __init__(self, address, username, password, port=22):
        self.cli = CLI()
        self.mode = CommandMode(r'#|\$|Destination|>')  # for example r'%\s*$'
        self.session_types = [SSHSession(host=address,
                                         username=username, password=password, port=port)]

        self.session = self.cli.get_session(command_mode=self.mode,
                                            defined_sessions=self.session_types)

    def send_command_list(self, command_list: List[str]) -> str:
        with self.session as my_session:
            outp = []
            for single_command in command_list:
                time.sleep(0.5)
                output = my_session.send_command(single_command)
                outp.append(output)
            out = '\n'.join(outp)
        return out

    def send_command(self, command) -> str:
        with self.session as my_session:
            out = my_session.send_command(command)
        return out


if __name__ == "__main__":
    cli = LinuxSSH("192.168.85.47", "root", "Password1", "22")
    outp = cli.send_command("hostname")
    print(outp.split("\n")[0].strip())