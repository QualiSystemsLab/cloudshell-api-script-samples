# Get Vcenter Cluster Info

Debug script to test vcenter shell command

## Usage

Add config data to config.py

```python
SERVER = "<CS_HOST>"
USER = "<CS_USER>"
PASSWORD = "<CS_PASSWORD>"
DOMAIN = "<CS_DOMAIN>"
VCENTER_DATASTORE = "<MY_DATASTORE>"
SANDBOX_ID = "<SANDBOX_ID>"
```

## Sample Response

```json
{
  "datastore": {
    "capacity": "5.46 TB",
    "used": "4.32 TB",
    "free": "4.32 TB",
    "used_percentage": "79"
  },
  "cpu": {
    "capacity": "35.20 GHz",
    "used": "5.85 GHz",
    "free": "29.35 GHz",
    "used_percentage": "17"
  },
  "ram": {
    "capacity": "383.94 GB",
    "used": "52.21 GB",
    "free": "331.73 GB",
    "used_percentage": "14"
  }
}
```