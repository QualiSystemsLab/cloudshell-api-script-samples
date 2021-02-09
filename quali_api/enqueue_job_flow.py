from _quali_api_wrapper import QualiAPISession
import json

with open('job1_data.json') as handle:
    job_data_dict = json.loads(handle.read())

api = QualiAPISession(host="localhost", username="admin", password="admin")

job_result = api.enqueue_job(job_data=job_data_dict)

print job_result
