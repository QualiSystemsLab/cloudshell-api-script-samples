"""
Convenience methods for printing to sandbox console and logging at same time
"""
from cloudshell.api.cloudshell_api import CloudShellAPISession
from logging import Logger


class SandboxReporter(object):
    def __init__(self, api, reservation_id, logger=None):
        """
        logger is optional, console printing can work without logger object
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
    def _info_log(self, message):
        if self._logger:
            self._logger.info(message)

    def info_out(self, message, log_only=False):
        """
        logger.info and print to console
        :param str message:
        :param bool log_only:
        :return:
        """
        self._info_log(message)
        if not log_only:
            self.sb_print(message)

    def debug_out(self, message, log_only=False):
        """
        logger.info and green print to console
        :param str message:
        :param bool log_only:
        :return:
        """
        if self._logger:
            self._logger.debug(message)
        if not log_only:
            self.sb_print(message)

    def warn_out(self, message, log_only=False):
        """
        logger.warning and yellow print to console
        :param str message:
        :param bool log_only:
        :return:
        """
        self._info_log(message)
        if not log_only:
            self.sb_warn_print(message)

    def err_out(self, message, log_only=False):
        """
        logger.error and red print to console
        :param str message:
        :param bool log_only:
        :return:
        """
        if self._logger:
            self._logger.error(message)
        if not log_only:
            self.sb_err_print(message)

    def exc_out(self, message, log_only=False):
        """
        logger.error and red print to console
        :param str message:
        :param bool log_only:
        :return:
        """
        if self._logger:
            self._logger.exception(message)
        if not log_only:
            self.sb_err_print(message)

    def success_out(self, message, log_only=False):
        """
        logger.info and green print to console
        :param str message:
        :param bool log_only:
        :return:
        """
        self._info_log(message)
        if not log_only:
            self.sb_success_print(message)

