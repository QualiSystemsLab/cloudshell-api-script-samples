# Commit Zip to Branch
When working with ansible playbook with multiple files, a zip archive needs to be committed to repo.

Some options to handle this pain point:
1. Create zip locally on dev machine and push source changes and zip together
2. Push source code, and have [gitlab-CI](commit-back-repo-gitlab-ci.yml) job detect change to playbook folder source code, create zip and commit
    - create access token for project and add as CI variable
    - this will create an additional commit to history
    - this also adds binary file into repo
    - need to remember to pull down the new "zip" commit before pushing new changes
3. Have similar CI job detect change and generate zip, but push to external web server hosting instead of commiting binary
   - this adds dependency of setting up another web server (can also use cloudshell IIS server)
   - Can pass in branch name to name of zip to have different hosted zips for testing
   - Firewall rules can be placed on IIS to only allow downloads from the Execution Server
   - cleaner option in terms of git history and storage


