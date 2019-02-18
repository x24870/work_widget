from bmcDesginReader import sheetReader
from pmcp_parser import PMCP_Parser

#Get adc var
reader = sheetReader()
reader.read_bmc_design_sheet('BMC_design.xlsx')

parser = PMCP_Parser()
parser.adc_handler.set_adc_par(reader.adc_par)
parser.adc_handler.get_adc_sensor_num(reader.sdr_list)
