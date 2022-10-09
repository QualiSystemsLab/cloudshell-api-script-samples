# Auto Generate Ansible Archive

When working
with [cloudshell ansible playbooks](https://help.quali.com/Online%20Help/0.0/Portal/Content/DevGuide/Config-Mng/Ansible.htm?tocpath=The%20CloudShell%20DevGuide%7CDeveloping%20Configuration%20Management%20Scripts%20for%20Apps%7CAnsible%20Playbook%20Development%20for%20Apps%7C_____0)
with site.yml and multiple files, a zip archive needs to be committed to repo.

Some options to handle this step:

1. Create zip locally on dev machine and push source changes and zip together
2. Push source code, and have [gitlab-CI](commit-back-repo-gitlab-ci.yml) job detect change to playbook folder source
   code, create zip and commit
    - create access token for project and add as CI variable
    - this will create an additional commit to history
    - this also adds binary file into repo
    - need to remember to pull down the new "zip" commit before pushing new changes
3. Have similar [CI job](zip-and-push-to-IIS-gitlab-ci.yml) detect change and generate zip, but push to external web
   server hosting instead of commiting binary. Then place link to web server on app instead of gitlab hosted link.
    - this adds dependency of setting up another web server (can also use cloudshell IIS server)
    - Can pass in branch name to name of zip to have different hosted zips for testing
    - Firewall rules can be placed on IIS to only allow downloads from the Execution Server
    - cleaner option in terms of git history and storage


