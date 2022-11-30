import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree


def get_element_tree_from_str(xml_str: str) -> ElementTree:
    """
    https://stackoverflow.com/a/18281386
    """
    return ET.ElementTree(ET.fromstring(xml_str))


def get_element_tree_from_file_path(file_path: str) -> ElementTree:
    return ET.parse(file_path)


def edit_vlan_id_in_tree(element_tree: ElementTree, target_service_model: str, new_vlan_id: str) -> ElementTree:
    """
    Iterate over services, find ServiceName that matches service model
    Iterate over the attributes, update the VLAN ID attribute
    write to tree
    """
    root_element = element_tree.getroot()
    for curr_service in root_element.iter("Service"):
        service_data: dict = curr_service.attrib
        if service_data["ServiceName"] != target_service_model:
            continue
        for curr_attr in curr_service.iter("Attribute"):
            attr_data: dict = curr_attr.attrib
            if attr_data["Name"] == "VLAN ID":
                attr_data["Value"] = new_vlan_id
                return element_tree
    raise ValueError("Target Service not found in Element Tree")


def update_xml_tree(xml_path: str, target_service_model: str, new_vlan_id: str):
    element_tree = get_element_tree_from_file_path(xml_path)
    element_tree = edit_vlan_id_in_tree(element_tree, target_service_model, new_vlan_id)
    element_tree.write(xml_path)


if __name__ == "__main__":
    TEST_TOPOLOGY_XML = """
        <TopologyInfo xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
          <Details Name="vlan dev" Alias="vlan dev" Driver="Python Setup &amp; Teardown" SetupDuration="10" TeardownDuration="10" Public="false" DefaultDuration="120" EnableSandboxSave="true" AbstractOnSavePolicy="Default" IsPersistentSandbox="false" TopologyId="f36c4723-8496-4d5b-9b61-8374d01c0fe2" BaseTopologyId="">
            <Description>Blueprint with preconfigured setup &amp; teardown processes.Deploys Apps and resolves connections on Setup, and deletes App VMs on Teardown</Description>
            <Categories />
            <Scripts>
              <Script Name="Default Sandbox Setup 4.0" />
            </Scripts>
            <Diagram Zoom="1" NodeSize="Medium" />
          </Details>
          <Services>
            <Service PositionX="1034.09091186523" PositionY="169.01136779785202" Alias="VLAN Manual" ServiceName="VLAN Manual">
              <Attributes>
                <Attribute Name="VLAN ID" Value="169" />
                <Attribute Name="Dummy Attr" Value="Hi" />
              </Attributes>
            </Service>
            <Service PositionX="100" PositionY="100" Alias="Dummy Service" ServiceName="DummyService">
              <Attributes>
                <Attribute Name="Dummy Attr 5" Value="179" />
                <Attribute Name="Dummy Attr" Value="Hi" />
              </Attributes>
            </Service>
          </Services>
          <Apps />
        </TopologyInfo>
    """
    element_tree = get_element_tree_from_str(TEST_TOPOLOGY_XML)
    element_tree = edit_vlan_id_in_tree(element_tree, "VLAN Manual", "66")
    root = element_tree.getroot()
    ET.indent(root)
    print(ET.tostring(root, encoding="unicode"))
