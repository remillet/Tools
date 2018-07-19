import xml.etree.ElementTree as ET
import sys

cspaceXML = ET.parse(sys.argv[1])
root = cspaceXML.getroot()
print ET.tostring(root)
