from cloudshell.api.cloudshell_api import CloudShellAPISession
import xml.etree.ElementTree as ET


def get_pretty_xml(xml_str: str) -> str:
    element = ET.XML(xml_str)
    ET.indent(element)
    return ET.tostring(element, encoding='unicode')


if __name__ == "__main__":
    api = CloudShellAPISession(host="localhost",
                               username="admin",
                               password="admin",
                               domain="Global")

    SANDBOX_ID = "92094f21-2178-4bf7-a0e3-70fa6a134917"
    SAMPLE_XML = "<xmp><data><dinner>pizza</dinner></data></xmp>"
    pretty_xml = get_pretty_xml(SAMPLE_XML)
    api.WriteMessageToReservationOutput(SANDBOX_ID, pretty_xml)
