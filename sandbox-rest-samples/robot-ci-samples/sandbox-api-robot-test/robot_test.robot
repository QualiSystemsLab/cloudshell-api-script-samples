*** Settings ***
Documentation    An example test suite passing in some variables from command line and printing to console

*** Variables ***
${sandbox_id}    <SANDBOX_ID>
${resource_ip}   0.0.0.0


*** Test Cases ***
Print Stuff
    Log To Console    Sandbox ID: ${sandbox_id}
    Log To Console    Resource IP: ${resource_ip}
