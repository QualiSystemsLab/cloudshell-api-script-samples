import requests

PORTAL_SERVER = "localhost"
EXECUTION_ID = "96303587-8a06-45d2-a9db-728368aa4cb7"

REPORT_LINK = F"http://{PORTAL_SERVER}/Test/Report?reportId={EXECUTION_ID}"


response = requests.get(REPORT_LINK)

with open(f'report_{EXECUTION_ID}.pdf', 'wb') as f:
    f.write(response.content)

print("done")
