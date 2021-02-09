from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.sandbox_print_helpers import *
import helper_code.automation_api_helpers as api_help
from cloudshell.api.cloudshell_api import CloudShellAPISession

# Importing all needed modules
from multiprocessing.pool import ThreadPool, AsyncResult
import time


# Starting timer for Parent measurement

# Define the function which will be executed within the ThreadPool
def async_execute(api, res_id, resource_name):
    """
    function to be passed to threading example
    :param CloudShellAPISession api:
    :return:
    """
    res = api.ExecuteCommand(reservationId=res_id,
                             targetName=resource_name,
                             targetType="Resource",
                             commandName="resource_timed_sleep",
                             printOutput=True)
    return res.Output


def get_error_str(result):
    """
    get error string without throwing error
    :param AsyncResult result:
    :return:
    """
    try:
        result.get()
    except Exception as e:
        return str(e)


# ========== Primary Function ==========
def first_module_flow(sandbox, components=None):
    """
    Functions passed into orchestration flow MUST have (sandbox, components) signature
    :param Sandbox sandbox:
    :param components
    :return:
    """
    api = sandbox.automation_api
    res_id = sandbox.id

    # start timer for parent process
    start_time = time.time()

    resources = api_help.get_reservation_resources(api, res_id)
    putshell_resources = [resource for resource in resources if resource.ResourceModelName == 'Putshell']

    thread_count = len(putshell_resources)  # Define the limit of concurrent running threads
    thread_pool = ThreadPool(processes=thread_count)  # Define the thread pool to keep track of the sub processes
    known_threads = {}

    # Now we execute 10 parallel threads
    for resource in putshell_resources:
        known_threads[resource.Name] = thread_pool.apply_async(async_execute, args=(api, res_id, resource.Name))

    thread_pool.close()

    # After all threads started we close the pool
    thread_pool.join()  # And wait until all threads are done

    # Getting the results of all threads
    failed_threads = {resource: get_error_str(result) for resource, result in known_threads.items()
                      if not result.successful()}

    if failed_threads:
        err_msg = "ERRORS OCCURED, SEE LOGS / ACTIVITY FEED FOR MORE INFO"
        warn_print(api, res_id, "===== " + err_msg + " =====")
        for key, value in failed_threads.items():
            # resource name is the key, error string is the value
            err_print(api, res_id, "===== '{}' ERROR =====".format(key))
            sb_print(api, res_id, value)
        sb_print(api, res_id, "====================")
        duration = time.time() - start_time
        sb_print(api, res_id, "Parent Process ran {} seconds".format(duration))
        raise Exception(err_msg)

    duration = time.time() - start_time
    sb_print(api, res_id, "Parent Process ran {} seconds".format(duration))
    pass
