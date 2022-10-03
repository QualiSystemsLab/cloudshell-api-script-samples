from cloudshell.api.cloudshell_api import CloudShellAPISession, InputNameValue

api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")

SANDBOX_ID = "20054710-42cb-4d04-bab0-214f93380b72"
RESOURCE_NAME = "<MY_CLOUDSHELL_RESOURCE>"
COMMAND_NAME = "<RESOURCE_COMMAND_NAME>"
COMMAND_INPUTS = [InputNameValue("Param1", "Value1"),
                  InputNameValue("Param2", "Value2")]

output = api.ExecuteCommand(reservationId=SANDBOX_ID,
                            targetName=RESOURCE_NAME,
                            targetType="Resource",
                            commandName=COMMAND_NAME,
                            commandInputs=COMMAND_INPUTS,
                            printOutput=True).Output

print(f"command output: {output}")
