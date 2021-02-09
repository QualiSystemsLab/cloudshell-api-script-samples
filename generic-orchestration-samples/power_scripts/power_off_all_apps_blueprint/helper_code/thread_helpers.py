from cloudshell.workflow.orchestration.sandbox import Sandbox
import time
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool
# from multiprocessing import Pool
from cloudshell.api.cloudshell_api import ResourceAttribute
from cloudshell.api.cloudshell_api import TopologyReservedResourceInfo


def partial_wrapper(sandbox, command_wrapper, device):
    """
    for adding partial arguments to function which is passed to map, device must be last argument
    :param Sandbox sandbox:
    :param function command_wrapper:
    :param TopologyReservedResourceInfo device:
    :return:
    """
    command_wrapper(sandbox, device)


def get_thread_results(sandbox, device_list, command_wrapper):
    """
    get results from threads for a desired command
    :param Sandbox sandbox:
    :param list of TopologyReservedResourceInfo device_list:
    :param function command_wrapper:
    :return:
    """
    thread_count = len(device_list)
    pool = ThreadPool(thread_count)

    # first argument to "partial" is the function you want to append the arguments to
    # then the following arguments are attached arguments
    # leaving the last spot open because map will pass the device to this function at runtime
    mapped_func = partial(partial_wrapper, sandbox, command_wrapper)
    results = pool.map(mapped_func, device_list)

    pool.close()
    pool.join()
    return results

