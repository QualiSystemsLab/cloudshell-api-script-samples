# Find sandbox ID from newly launched job
This script is a method to obtain sandbox id of newly formed job.
Methodology is to pass in a UUID as global input, then to query sandbox REST api for sandbox with matching input value

## To use
Import "sandbox_id_from_suite.get_sandbox_id_from_job" function and pass in data.  See implementation example at bottom of file

Sample output from script:
```commandline
starting new job, passing '123456789' as custom UUID
suite started: 0a15b2a2-8d02-49f7-9b97-3e1774c6eecd
searching for job's sandbox...
sandbox id found after '0.17815279999999944' seconds
sandbox id: 9bfc7d0a-f15d-4feb-9150-55d46c574ad2
```

## Notes
- Sandbox Api server may not be hosted on quali server, it is typically hosted together with Portal server
  - https://help.quali.com/Online%20Help/0.0/Portal/Content/IG/Overview/cs-reqd-ports.htm?Highlight=ports