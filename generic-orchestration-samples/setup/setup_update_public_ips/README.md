# Setup eDTM
Setup will provision and register Ginger Execution agents to the Agent Handler URL. 

## Setup Flow
1. Provision one Linux VM per Execution Agent
2. Run config script to Install Docker
3. Read IP of agent handler from sandbox and pass into config script to run container and register with handler

## NOTES
Run container config script param:
- EXECUTION_HANDLER_URL

Docker install script:
https://raw.githubusercontent.com/docker/docker-install/master/rootless-install.sh

Ginger install script:
https://raw.githubusercontent.com/QualiSystemsLab/App-Configuration-Demo-Scripts/master/ginger/register_ginger.sh

