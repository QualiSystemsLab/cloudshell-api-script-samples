# Setup set user mail on apps
This is sample script for getting user email and updating config parameter on target apps

## To use
Set the following attribute on Generic Attribute Family
- `Update Mail` (boolean, default false)

App param on app and in script should be the following: `USER_MAIL`

Upload script as setup, python 2 or 3 both fine, and replace setup on target blueprint.

Note in main.py how default config is disabled and this is replacing it.

For info on syntax to collect variables inside script see examples:
- [dev guide](https://help.quali.com/Online%20Help/0.0/Portal/Content/DevGuide/Config-Mng/Custom-Scripts.htm?tocpath=The%20CloudShell%20DevGuide%7CDeveloping%20Configuration%20Management%20Scripts%20for%20Apps%7CCustom%20Script%20Development%20for%20Apps%7C_____0)
- [usage example](https://github.com/QualiSystemsLab/App-Configuration-Demo-Scripts/blob/master/print_email_param.sh)
