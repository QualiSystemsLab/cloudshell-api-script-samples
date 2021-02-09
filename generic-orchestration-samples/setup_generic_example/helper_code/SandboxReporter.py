"""
Convenience methods for printing to sandbox console and logging at same time
"""
from cloudshell.api.cloudshell_api import CloudShellAPISession
from cloudshell.logging.qs_logger import get_qs_logger
from logging import Logger
import inspect


class SandboxReporter(object):
    def __init__(self, api, reservation_id, logger=None):
        """
        logger is optional, console printing can work without logger object
        exception will be thrown for logger methods called if no logger is added at instantiation
        :param CloudShellAPISession api:
        :param str reservation_id:
        :param Logger logger:
        """
        self._api = api
        self._reservation_id = reservation_id
        self._logger = logger

    # ==== PRINT TO SANDBOX CONSOLE HELPERS ===
    def sb_print(self, message):
        """
        alias method for printing to reservation output
        :param str message:
        :return:
        """
        self._api.WriteMessageToReservationOutput(self._reservation_id, message)

    @staticmethod
    def _html_wrap(content, color, elm):
        return "<{elm} style='color: {color}'>{content}</{elm}>".format(content=content,
                                                                        elm=elm,
                                                                        color=color)

    def sb_html_print(self, message, txt_color="white", html_elm="span"):
        """
        for wrapping message in custom html color and sizing
        pass in
        :param str message:
        :param str txt_color: choose general color name or hex string
        :param str html_elm: select html element ex. 'h2', 'p', 'em'
        :return:
        """
        wrapped_message = self._html_wrap(message, txt_color, html_elm)
        self.sb_print(wrapped_message)

    def sb_err_print(self, message):
        """
        print red message for errors
        :param str message:
        :return:
        """
        self.sb_html_print(message, "red", "span")

    def sb_success_print(self, message):
        """
        print green message for success statements
        :param str message:
        :return:
        """
        self.sb_html_print(message, "#4BB543", "span")

    def sb_warn_print(self, message):
        """
        print yellow message for alerting actions
        :param str message:
        :return:
        """
        self.sb_html_print(message, "yellow", "span")

    def sb_link_print(self, url, text):
        """
        for wrapping text in html anchor tag; opens link in new tab by default
        :param str url:
        :param str text: the link text to be displayed
        :return:
        """
        def html_link_wrap(target_url, link_text):
            return """<a href={url} 
                   style="text-decoration: underline"
                   target = "_blank"
                   rel = "noopener noreferrer"
                   >{link_text}</a>""".format(url=target_url, link_text=link_text)

        wrapped_link = html_link_wrap(url, text)
        self.sb_print(wrapped_link)

    # ==== LOGGING AND PRINTING ====
    @staticmethod
    def _prepend_func_data(message):
        """
        rename the public class function to it's caller
        this is so the function names get logged correctly by QS Logger
        Otherwise they would all be logged with the wrapper name
        """
        stack = inspect.stack()
        parent_func = stack[2]
        full_path = parent_func[1]
        module_name = full_path.split("/")[-1].split(".py")[0]
        line_number = parent_func[2]
        parent_func_name = parent_func[3]
        function_data = "{}.{}.{}".format(module_name, parent_func_name, line_number)
        message = "{:<40} {:>}".format(function_data, message)
        return message

    def _validate_logger(self):
        if not self._logger:
            raise Exception("Can not perform log operation. No logger instance passed to SandboxReporter")

    def info_out(self, message):
        log_message = self._prepend_func_data(message)
        self._validate_logger()
        self._logger.info(log_message)
        self.sb_print(message)

    def warn_out(self, message):
        log_message = self._prepend_func_data(message)
        self._validate_logger()
        self._logger.warning(log_message)
        self.sb_warn_print(message)

    def err_out(self, message):
        log_message = self._prepend_func_data(message)
        self._validate_logger()
        self._logger.error(log_message)
        self.sb_err_print(message)

    def success_out(self, message):
        log_message = self._prepend_func_data(message)
        self._validate_logger()
        self._logger.info(log_message)
        self.sb_success_print(message)


if __name__ == "__main__":
    LIVE_SANDBOX_ID = "39e83e10-3613-425e-b4db-591a34acd193"
    session = CloudShellAPISession("localhost", "admin", "admin", "Global")
    logger = get_qs_logger(log_group=LIVE_SANDBOX_ID)
    reporter = SandboxReporter(session, LIVE_SANDBOX_ID, logger)
    def my_func():
        reporter.info_out("here we go")
        reporter.warn_out("here we go")
        reporter.err_out("here we go")
        reporter.success_out("here we go")
    my_func()