from cloudshell.helpers.scripts.cloudshell_scripts_helpers import get_reservation_context_details, get_api_session, \
    get_resource_context_details
from cloudshell.logging.qs_logger import get_qs_logger
from cloudshell.helpers.sandbox_reporter.reporter import SandboxReporter
from traceroute_helper import run_traceroute_to_ip, get_local_ip


class TraceRouteException(Exception):
    pass


def run_es_traceroute():
    api = get_api_session()
    sb_details = get_reservation_context_details()
    sb_id = sb_details.id

    resource_details = get_resource_context_details()
    resource_name = resource_details.name
    logger = get_qs_logger(log_group=sb_id, log_category=resource_details.model, log_file_prefix=resource_name)
    reporter = SandboxReporter(api, sb_id, logger)
    ip = resource_details.address
    es_ip = get_local_ip()

    reporter.info(f"Running traceroute to '{resource_name}' at IP '{ip}' from Execution Server...")

    try:
        tr_output = run_traceroute_to_ip(ip)
    except Exception as e:
        msg = f"Failed ping to '{resource_name}' at IP '{ip}' from ES at IP '{es_ip}'.\n{str(e)}"
        reporter.error(msg)
        raise TraceRouteException(msg)

    print(tr_output)
