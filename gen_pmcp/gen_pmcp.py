import xml.etree.ElementTree as ET


tree = ET.parse('Wolfpass.pmc')
#tree = ET.parse('example.xml')
root = tree.getroot()
print(root.tag)
print(root.attrib)

for device in root.iter('device'):
    print(device)
    for child in device:
        print(child)
    print('---------------------')