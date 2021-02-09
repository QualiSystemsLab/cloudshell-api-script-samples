from cloudshell.api.cloudshell_api import CloudShellAPISession
from cloudshell.logging.qs_logger import get_qs_logger
from SandboxReporter import SandboxReporter

if __name__ == "__main__":
    LIVE_SANDBOX_ID = "39e83e10-3613-425e-b4db-591a34acd193"
    session = CloudShellAPISession("localhost", "admin", "admin", "Global")
    # session.WriteMessageToReservationOutput(LIVE_SANDBOX_ID, "hello")
    logger = get_qs_logger(log_group=LIVE_SANDBOX_ID)
    reporter = SandboxReporter(session, LIVE_SANDBOX_ID, logger)
    def my_func():
        reporter.info_out("here we go")
        reporter.warn_out("here we go")
        reporter.err_out("here we go")
        reporter.success_out("here we go")
    my_func()