from cloudshell.workflow.orchestration.sandbox import Sandbox
from custom_helpers import sb_print
from custom_helpers import get_reservation_resources


# ========== Primary Function ==========
def run_custom_setup(sandbox, components):
    """
    :param Sandbox sandbox:
    :param components
    :return:
    """
    resources = get_reservation_resources(sandbox)
    resources_count = str(len(resources))
    sb_print(sandbox, "resources in sandbox: {resources_count}".format(resources_count=resources_count))
