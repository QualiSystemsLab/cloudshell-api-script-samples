# Setup set user mail on apps
This is sample script for getting user email and updating config parameter on target apps

## To use
Set the following attribute on Generic Attribute Family
`Update Mail`
  - boolean, default false

App param should be the following:
`USER_MAIL`

Upload script as setup, python 2 or 3 both fine, and replace setup on target blueprint.

Note in main.py how default config is disabled and this is replacing it.