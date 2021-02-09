from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

res_id = "2aba8422-f6b8-4dd8-9cae-b3d136db62fe"

def get_global_input_val(input_key, inputs):
    input_search = [input.Value for input in inputs if input.ParamName == input_key]
    if input_search:
        input_val = input_search[0]
        return input_val
    else:
        raise Exception("can't find global input with key: '{}'".format(input_key))

inputs = api.GetReservationInputs(reservationId=res_id).GlobalInputs
app_id_val = get_global_input_val("app_id")

pass