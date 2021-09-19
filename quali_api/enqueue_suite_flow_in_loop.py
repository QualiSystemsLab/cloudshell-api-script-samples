from quali_api_wrapper import QualiAPISession
import json

with open('suite_data_hello_world.json') as handle:
    suite_data_dict = json.loads(handle.read())

api = QualiAPISession(host="localhost", username="admin", password="admin")

for i in range(5):
    print("starting suite number: #{}".format(i+1))
    suite_id = api.enqueue_suite(suite_data=suite_data_dict)
    suite_details = api.get_suite_details(suite_id)

    print("suite id: " + suite_id)
    print("===== suite details =====")
    print(suite_details)
print("All suites queued up")