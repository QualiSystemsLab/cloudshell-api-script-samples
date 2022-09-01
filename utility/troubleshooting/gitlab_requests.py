"""
helper script to try out request to private gitlab repo, as referenced in Quali custom script driver
https://github.com/QualiSystems/CustomScript-Shell/blob/877d0df447bf513088779d247116087ee14f63a4/package/cloudshell/cm/customscript/domain/script_downloader.py#L75
"""

import requests

TOKEN = "MY_TOKEN"
URL = "MY_URL"
headers = {"Private-Token": f"Bearer {TOKEN}"}
response = requests.get(URL, stream=True, headers=headers, verify=False)
print(f"Response code: {response.status_code}")
print(f"Response text:\n{response.text}")