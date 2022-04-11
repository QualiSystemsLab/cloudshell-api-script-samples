"""
1. Set SCRIPT_TYPE; choose from ["default", "setup", "teardown", "resource", "service"].
2. Set DEBUG_MODE to Boolean True for developing against live sandbox.
3. Take LIVE_SANDBOX_ID from sandbox URL.
NOTE: Set debug_mode to False before loading to Cloudshell portal.
      Running load_to_cs.py does this step automatically.
"""

SCRIPT_TYPE = "setup"
DEBUG_MODE = False
LIVE_SANDBOX_ID = "cbc2037a-381b-4d43-84c3-9d375339329b"

# Only relevant to set for "resource" OR "service" type scripts
TARGET_RESOURCE_NAME = None
TARGET_SERVICE_NAME = None


