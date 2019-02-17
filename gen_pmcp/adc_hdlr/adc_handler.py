import os
import xml.etree.ElementTree as ET

REPLACE_DEFAULT_CONF = [
    'SENSOR_NUM',
    'ID_STR',
]

REPLACE_DEFAULT_SDR_CONF = [
    'M_VAL',
    'UPPER_NON_RECOVERABLE',
    'UPPER_CRITICAL',
    'UPPER_NON_CRITICAL',
    'LOWER_NON_RECOVERABLE',
    'LOWER_CRITICAL',
    'LOWER_NON_CRITICAL',
]

class adc_hdlr():
    def __init__(self, module_path):
        self.tree = ET.parse(os.path.join(module_path, 'adc_sample.xml'))
        self.root = self.tree.getroot()
        self.connection_tree = ET.parse(os.path.join(module_path, 'adc_connection_sample.xml'))
        self.connection_root = self.connection_tree.getroot()
        self.sdr_data = {}

    def device_hdlr(self):
        self.root.find('./name').text = 'TODO'#TODO: replace the value according bmc design sheet

        for config in self.root.findall('./config'):
            if config[0].text in REPLACE_DEFAULT_CONF:
                config[1].text = 'TODO'#TODO: replace the value according bmc design sheet

        self.root.find('./sdr/name').text = 'TODO'#TODO: replace the value according bmc design sheet

        for config in self.root.findall('./sdr/config'):
            if config[0].text in REPLACE_DEFAULT_SDR_CONF:
                config[1].text = 'TODO'#TODO: replace the value according bmc design sheet

if __name__ == "__main__":
    hdlr = adc_hdlr('.')
    hdlr.device_hdlr()
    hdlr.tree.write('output.xml')
