import requests


PACKAGE_PATH = r"C:\Users\natti.k\Downloads\CloudShell Sandbox Template2\CloudShell Sandbox Template2.zip"
CS_SERVER = "192.168.85.74"

# login get token
r = requests.put(f'http://{CS_SERVER}:9000/Api/Auth/Login', {"username": "admin", "password": "admin", "domain": "Global"})
authcode = "Basic " + r.text[1:-1]


# 2 Open the package before import
fileobj = open(PACKAGE_PATH, 'rb')

# 3 Send to CloudShell by calling Import Package REST API
r = requests.post(f'http://{CS_SERVER}:9000/API/Package/ImportPackage',
                  headers={"Authorization": authcode},
                  files={"file": fileobj})
print(r.text)
print(r.ok)