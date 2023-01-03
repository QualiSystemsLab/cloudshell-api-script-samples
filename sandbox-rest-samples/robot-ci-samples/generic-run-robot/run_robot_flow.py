"""
start sandbox, then run robot test, passing in sandbox id
https://stackoverflow.com/a/40394515
"""
import robot

robot.run("robot_test.robot", variable=["arg1:hello", "arg2:there", "arg3:friend"])
