# DB backup scripts
A collection of utility scripts to back up Cloudshell DBs

## MongoDB batch backup
- runs mongodump for 3 quali Mongo DBs, passing in Date as parameter for target parent folder
- sample assumes auth is set on DB, can be removed for non auth DB
- Example assuming default path of local embedded Mongo Server and running from the Mongo Server
- https://stackoverflow.com/a/60282671


```
mongodump --host <host-ip> --port 27017 --db <database>  --authenticationDatabase admin --username <username> --password <password> --out ./Documents/
```

example:
Change Date of Parent backup folder
```
mongodump --host localhost --port 27017 --db Quali  --authenticationDatabase admin --username QualiAdmin --password QualiAdminPassword --out C:\MongoDumpBackups\20_11_2022

mongodump --host localhost --port 27017 --db QualiLogs  --authenticationDatabase admin --username QualiAdmin --password QualiAdminPassword --out C:\MongoDumpBackups\20_11_2022

mongodump --host localhost --port 27017 --db QualiSandboxService  --authenticationDatabase admin --username QualiAdmin --password QualiAdminPassword --out C:\MongoDumpBackups\20_11_2022
```

Bash script example passing in Date as param
- assuming that script is run against localhost
- note that credentials are hardcoded. May want to parametrize this
```
DATE_FOLDER = ${1}
mongodump --host localhost --port 27017 --db Quali  --authenticationDatabase admin --username QualiAdmin --password QualiAdminPassword --out C:\MongoDumpBackups\${DATE_FOLDER}

mongodump --host localhost --port 27017 --db QualiLogs  --authenticationDatabase admin --username QualiAdmin --password QualiAdminPassword --out C:\MongoDumpBackups\${DATE_FOLDER}

mongodump --host localhost --port 27017 --db QualiSandboxService  --authenticationDatabase admin --username QualiAdmin --password QualiAdminPassword --out C:\MongoDumpBackups\${DATE_FOLDER}
```