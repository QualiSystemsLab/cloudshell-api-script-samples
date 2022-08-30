"""
utility script to install all shells in current directory
"""
import json
import os
import subprocess


curr_dir = os.path.dirname(os.path.abspath(__file__))
shells = [x for x in os.listdir()
          if not x.endswith(".py")]

print(f"Installing {len(shells)} shells:\n{json.dumps(shells, indent=4)}")

for shell in shells:
    full_path = os.path.join(curr_dir, shell)
    os.chdir(full_path)
    print(f"installing {shell}...")
    subprocess.run(["shellfoundry", "install"])
    print("================")

print("Script Done.")
