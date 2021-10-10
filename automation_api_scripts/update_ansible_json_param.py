import json

from cloudshell.api.cloudshell_api import ConfigParam, CloudShellAPISession, AppConfiguration

# static environment data - this will be pulled dynamically from sandbox in orchestration script
DEPLOYED_APP_NAME = "<MY_APP_NAME>"
JSON_PAYLOAD_PARAM_NAME = "<MY_JSON_PARAM>"
SANDBOX_ID = "<LIVE_SANDBOX_ID>"

api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")

# some mock data to forward as json
my_data_dict = {
    "key1": "value1",
    "key2": "value2",
}

# serialize to json
my_json = json.dumps(my_data_dict)

# explicitly wrap with single quotes to be valid json when written to playbook vars file
ansible_json_var = "'{}'".format(my_json)

config_params = [ConfigParam(Name=JSON_PAYLOAD_PARAM_NAME, Value=ansible_json_var)]
config = AppConfiguration(AppName=DEPLOYED_APP_NAME, ConfigParams=config_params)
api.ConfigureApps(reservationId=SANDBOX_ID, appConfigurations=[config], printOutput=True)
