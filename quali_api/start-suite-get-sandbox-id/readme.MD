# Find sandbox ID from newly launched job
This script is a method to obtain sandbox id of newly formed job.
Methodology is to pass in a UUID as global input, then to query sandbox REST api for sandbox with matching input value

## To use
Import "sandbox_id_from_suite.get_sandbox_id_from_job" function and pass in data.  See implementation example at bottom of file

## Notes
- Sandbox Api server may not be hosted on quali server, it is typically hosted together with Portal server
  - https://help.quali.com/Online%20Help/0.0/Portal/Content/IG/Overview/cs-reqd-ports.htm?Highlight=ports