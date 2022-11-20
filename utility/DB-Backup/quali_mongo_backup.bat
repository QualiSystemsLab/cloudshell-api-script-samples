set DATE_FOLDER=%1

"C:\Program Files\MongoDB\Server\4.2\bin\mongodump.exe" --host localhost --port 27017 --db Quali --out C:\MongoDumpBackups\%DATE_FOLDER%

"C:\Program Files\MongoDB\Server\4.2\bin\mongodump.exe" --host localhost --port 27017 --db QualiLog --out C:\MongoDumpBackups\%DATE_FOLDER%

"C:\Program Files\MongoDB\Server\4.2\bin\mongodump.exe" --host localhost --port 27017 --db QualiSandboxService --out C:\MongoDumpBackups\%DATE_FOLDER%
