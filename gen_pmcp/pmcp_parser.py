import os
import xml.etree.ElementTree as ET

from adc_hdlr import adc_handler

class PMCP_Parser():
    def __init__(self):
        self.tree = None
        self.root = None
        self.adc_handler = adc_handler.adc_hdlr(os.path.join(os.getcwd(), 'adc_hdlr'))

    def read_pmc(self, filename):
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()

    def clear_all_devices(self, remain_asd2500_chip=True):
        devcfg_root = self.root.find('devcfg')

        for device in devcfg_root.findall('device'):
            if 'AST2500' in device.find('name').text:
                continue
            devcfg_root.remove(device)

        for device in devcfg_root.findall('device_connection'):
            if 'AST2500' in device.find('name').text:
                continue
            devcfg_root.remove(device)
        return

    def gen_prefix(self):
        xml_head = '<?xml version= "1.0" encoding="ISO-8859-1"?>\n<?MDS version= "1.8"?>'
        return

    def test(self):
        devcfg_root = self.root.find('devcfg')
        newTree = ET.ElementTree()
        newTree._setroot(devcfg_root)
        newTree.write('test.xml')

if __name__ == "__main__":
    parser = PMCP_Parser()
    parser.read_pmc('Wolfpass.pmc')
    #parser.clear_all_devices()
    #parser.tree.write('output.xml')
    #parser.test()
    
    adc_handler = adc_handler.adc_hdlr(os.path.join(os.getcwd(), 'adc_hdlr'))
