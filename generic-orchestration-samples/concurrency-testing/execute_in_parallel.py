from multiprocessing.dummy import Pool as ThreadPool
from cloudshell.api.cloudshell_api import InputNameValue, CloudShellAPISession


def _execute_resource_command(api, res_id, resource_name, command_name, command_inputs, target_type):
    '''
     :param CloudShellAPISession api:
     :param components:
     :return:
     '''
    try:
        api.ExecuteCommand(reservationId=res_id,
                           targetName=resource_name,
                           targetType=target_type,
                           commandName=command_name,
                           commandInputs=command_inputs,
                           printOutput=True)
    except Exception as e:
        api.WriteMessageToReservationOutput(res_id, "Command '{}' failed with error: {}".format(command_name, str(e)))
        raise

def execute_command_in_parallel(resource_names, api, res_id, command_name, command_inputs, target_type):
    """
    execute same command on list of resources in parallel
    :param list[str] resource_names:
    :param CloudShellAPISession api:
    :param str res_id:
    :param str command_name:
    :param list[InputNameValue] command_inputs:
    :param str target_type:
    :return:
    """
    number_of_services = len(resource_names)
    if number_of_services > 0:
        pool = ThreadPool(number_of_services)
        async_data = [(resource_name, pool.apply_async(_execute_resource_command, (api,
                                                                                      res_id,
                                                                                      resource_name,
                                                                                      command_name,
                                                                                      command_inputs,
                                                                                      target_type)))
                         for resource_name in resource_names]

        pool.close()
        pool.join()

        result_exceptions = []
        result_successes = []
        for data in async_data:
            resource_name = data[0]
            async_response = data[1]
            try:
                result = async_response.get()
            except Exception as e:
                result_exceptions.append((resource_name, str(e)))
            else:
                result_successes.append((resource_name, result))

        if result_exceptions:
            exception_resource_names = [r[0] for r in result_exceptions]
            raise Exception("Exceptions thrown running '{}' for following resources: {}".format(command_name,
                                                                                                exception_resource_names))


if __name__ == "__main__":
    LIVE_SANDBOX_ID = "94f4841f-08c4-42d8-94a4-30b76f992666"

    api = CloudShellAPISession("localhost", "admin", "admin", "Global")
    execute_command_in_parallel(resource_names=["mock_1", "mock_2", "mock_3"],
                                api=api,
                                res_id=LIVE_SANDBOX_ID,
                                command_name="throw_exception",
                                command_inputs=[],
                                target_type="Resource")
