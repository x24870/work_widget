import xml.etree.ElementTree as ET


tree = ET.parse('WolfpassEmp.pmc')
root = tree.getroot()
devcfg_root = root.find('devcfg')

for device in devcfg_root.findall('device'):
    print(device)
    devcfg_root.remove(device)

for device in devcfg_root.findall('device_connection'):
    print(device)
    devcfg_root.remove(device)


tree.write('output.xml')


