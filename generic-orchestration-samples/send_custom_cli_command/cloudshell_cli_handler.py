from cloudshell.cli.service.cli import CLI
from cloudshell.cli.session.ssh_session import SSHSession
from cloudshell.cli.service.command_mode import CommandMode


class CreateSession():
    COMMAND_MODE_PROMPT = r'#'

    def __init__(self, host, username, password, logger=None):
        """
        :param host:
        :param username:
        :param password:
        :param logger:
        """
        self.cli = CLI()
        self.logger = logger
        self.mode = CommandMode(prompt=self.COMMAND_MODE_PROMPT)  # for example r'%\s*$'
        self.session_types = [SSHSession(host=host, username=username, password=password)]
        self.session = self.cli.get_session(command_mode=self.mode,
                                            defined_sessions=self.session_types)

    def send_terminal_command(self, single_command, action_map=None, error_map=None):
        """
        :param str single_command:
        :return:
        """
        if not isinstance(single_command, str):
            raise Exception("Expected string input for command. Received type {}, {}.".format(type(single_command),
                                                                                              str(single_command)))
        with self.session as my_session:
            outp = self._send_single_command(my_session, single_command, action_map, error_map)
            return r"{}".format(outp)

    def send_commands_list(self, commands_list):
        """
        iterate over list and return concatenated output
        :param list commands_list:
        :return:
        """
        if not isinstance(commands_list, list):
            raise Exception("this method accepts a list. Input: {}".format(commands_list))
        multi_command_outp = []
        with self.session as my_session:
            if isinstance(commands_list, list):
                for single_command in commands_list:
                    outp = self._send_single_command(my_session, single_command)
                    multi_command_outp.append(outp)
                final_outp = '\n'.join(multi_command_outp)
                return r"{}".format(final_outp)

    def _send_single_command(self, session, single_command, action_map=None, error_map=None):
        """

        :param session:
        :param single_command:
        :return:
        """
        single_command = '{}'.format(single_command)
        if self.logger:
            self.logger.info('sending command {}'.format(single_command))
        current_outp = session.send_command(single_command, action_map=action_map, error_map=error_map)
        if self.logger:
            self.logger.info('got output {}'.format(current_outp))
        return current_outp


if __name__ == "__main__":
    host = "192.168.85.47"
    username = "root"
    password = "qs1234"
    cli = CreateSession(host, username, password)

    print("=== single command ===")
    sample_command = 'hostname -I'
    outp = cli.send_terminal_command(sample_command)
    print(outp)

    print("=== multiple commands")
    sample_commands = ['hostname -I', "ifconfig"]
    outp = cli.send_commands_list(sample_commands)
    print(outp)
