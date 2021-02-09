import json

from time import sleep

from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

LIVE_SANDBOX_ID = ""

owner_id = "admin"
pool_id = "test_pool"
pool_length = 20

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

request = {
    "type": "NextAvailableNumericRangeFromRange",
    "poolId": pool_id,
    "reservationId": "",
    "ownerId": owner_id,
    "isolation": "Exclusive",
    "requestedRange": {
        "start": 1,
        "end": 3
    }
}

pool_set_res = api.CheckoutFromPool(selectionCriteriaJson=json.dumps(request))
pool_release_res = api.ReleaseFromPool(values=[],
                                       reservationId="",
                                       ownerId=owner_id,
                                       poolId=pool_id)
pass
