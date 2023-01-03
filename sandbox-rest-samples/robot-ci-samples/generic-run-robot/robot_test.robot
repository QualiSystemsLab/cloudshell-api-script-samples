*** Settings ***
Documentation    An example test suite passing in some variables from command line and printing to console

*** Variables ***
${arg1}    THIS
${arg2}    IS
${arg3}    SPARTA

*** Test Cases ***
Print Stuff
    Log To Console    ${arg1}
    Log To Console    ${arg2}
    Log To Console    ${arg3}
