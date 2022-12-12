# Delete Sandboxes / Blueprints

Scripts to delete ALL sandboxes / blueprints, or a subset based on criteria (such as belonging to target users)

## Dependencies
- Python version 3.7
- package requirements:
  - cloudshell-automation-api
    
## Delete ALL sandboxes
Deletes all historical sandboxes. Time range can be passed in. Default range is set to 2015 - 2025.

`python delete_ALL_sandboxes.py --help`
```
usage: Delete ALL sandboxes [-h] -s SERVER -u USER -p PASSWORD [--from FROM]
                            [--until UNTIL]

Automation API script to delete sandboxes

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Cloudshell Server User
  -u USER, --user USER  Cloudshell Server Password
  -p PASSWORD, --password PASSWORD
                        Cloudshell Server IP or DNS name
  --from FROM           start range. format MM/DD/YYYY HH:MM, ex. 01/01/2015
                        00:00
  --until UNTIL         end range. format MM/DD/YYYY HH:MM, ex. 01/01/2025
                        00:00
```
Sample commands:
`python delete_ALL_sandboxes.py -s localhost -u admin -p admin`
`python delete_ALL_sandboxes.py -s localhost -u admin -p admin --from 01/01/2020 --until 01/01/2021`

Sample command:
`python delete_ALL_blueprints.py -s localhost -u admin -p admin`

## Delete Sandboxes with Target Users
Accepts a list of cloudshell users. Deletes sandboxes owned by one of target users, OR has a target user as  permitted user

`python delete_sandboxes_with_target_users.py --help`

```
usage: Delete sandboxes for target users [-h] -s SERVER -u USER -p PASSWORD
                                         [--from FROM] [--until UNTIL] --users
                                         USERS

Automation API script to delete sandboxes

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Cloudshell Server User
  -u USER, --user USER  Cloudshell Server Password
  -p PASSWORD, --password PASSWORD
                        Cloudshell Server IP or DNS name
  --from FROM           start range. format MM/DD/YYYY HH:MM, ex. 01/01/2015
                        00:00
  --until UNTIL         end range. format MM/DD/YYYY HH:MM, ex. 01/01/2025
                        00:00
  --users USERS         list of space separated cloudshell users. Example:
                        user1 user2 user3.

```

Sample commands:
`python delete_sandboxes_with_target_users.py -s localhost -u admin -p admin --users user1 user2 user3`
`python delete_sandboxes_with_target_users.py -s localhost -u admin -p admin --users user1 user2 user3 --from 01/01/2020 --until 01/01/2021`

## Delete Blueprints with Target Users
Accepts list of cloudshell users. Deletes blueprints owned by one of specified users.

`python delete_blueprints_owned_by_users.py --help`

```
usage: Delete ALL blueprints [-h] -s SERVER -u USER -p PASSWORD --users USERS

Automation API script to delete blueprints

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Cloudshell Server User
  -u USER, --user USER  Cloudshell Server Password
  -p PASSWORD, --password PASSWORD
                        Cloudshell Server IP or DNS name
  --users USERS         list of space separated cloudshell users. Example:
                        user1 user2 user3.
```

sample command:
`python delete_blueprints_owned_by_users.py -s localhost -u admin -p admin --users user1 user2 user3`