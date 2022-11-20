set DATE_FOLDER=%1

mongodump --host localhost --port 27017 --db Quali  --authenticationDatabase admin --username QualiAdmin --password QualiAdminPassword --out C:\MongoDumpBackups\%DATE_FOLDER%

mongodump --host localhost --port 27017 --db QualiLog  --authenticationDatabase admin --username QualiAdmin --password QualiAdminPassword --out C:\MongoDumpBackups\%DATE_FOLDER%

mongodump --host localhost --port 27017 --db QualiSandboxService  --authenticationDatabase admin --username QualiAdmin --password QualiAdminPassword --out C:\MongoDumpBackups\%DATE_FOLDER%