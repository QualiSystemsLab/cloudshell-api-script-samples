from quali_api_wrapper import QualiAPISession
import json

with open('suite_data.json') as handle:
    suite_data_dict = json.loads(handle.read())

api = QualiAPISession(host="localhost", username="admin", password="admin")

suite_id = api.enqueue_suite(suite_data=suite_data_dict)
suite_details = api.get_suite_details(suite_id)

print "suite id: " + suite_id
print "===== suite details ====="
print suite_details
