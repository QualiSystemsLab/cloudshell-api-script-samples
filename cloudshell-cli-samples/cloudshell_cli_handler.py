from cloudshell.cli.service.cli import CLI
from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.cli.service.command_mode import CommandMode


class CreateSession():
    def __init__(self, host, username, password, logger=None, base_mode="#"):
        self.cli = CLI()
        self.logger = logger
        self.mode = CommandMode(fr'{base_mode}')  # for example r'%\s*$'
        enable_action_map = {
            "[Pp]assword for {}".format(username): lambda session, logger: session.send_line(password, logger)}
        self.elevated_mode = CommandMode(r'(?:(?!\)).)#\s*$', enter_command='sudo su', exit_command='exit',
                                         enter_action_map=enable_action_map)
        self.mode.add_child_node(self.elevated_mode)
        self.elevated_mode.add_parent_mode(self.mode)
        self.session_types = [SSHSession(host=host,
                                         username=username,
                                         password=password)]

        self.session = self.cli.get_session(command_mode=self.mode,
                                            defined_sessions=self.session_types)

    def send_terminal_command(self, command, password=None):
        outp = []
        out = None
        with self.session as my_session:
            if isinstance(command, list):
                for single_command in command:
                    if password:
                        single_command = '{command}'.format(command=single_command, password=password)
                        # single_command = 'echo {password} | sudo -S sh -c "{command}"'.format(command=single_command,
                        #                                                               password=password)
                    self.logger.info('sending command {}'.format(single_command))
                    current_outp = my_session.send_command(single_command)
                    outp.append(current_outp)
                    self.logger.info('got output {}'.format(current_outp))
                    out = '\n'.join(outp)
            else:
                if password:
                    command = '{command}'.format(command=command)
                out = my_session.send_command(command)
            return out


if __name__ == "__main__":
    import cli_credentials

    # juniper switch example
    base_mode = "%"
    cli = CreateSession(host=cli_credentials.HOST,
                        username=cli_credentials.USER,
                        password=cli_credentials.PASSWORD,
                        base_mode=base_mode)
    sample_command = 'ls'
    outp = cli.send_terminal_command(sample_command)
    print(outp)