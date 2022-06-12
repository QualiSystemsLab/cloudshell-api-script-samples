from port_from_connector import get_port_from_connector_alias
import os

TARGET_ALIAS_PARAM = "target_alias"


target_alias = os.environ.get(TARGET_ALIAS_PARAM)
if not target_alias:
    raise ValueError(f"No value received for param '{TARGET_ALIAS_PARAM}'")

get_port_from_connector_alias(target_alias)
