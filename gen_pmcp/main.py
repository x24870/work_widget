from bmcDesginReader import sheetReader

reader = sheetReader()
reader.read_bmc_design_sheet('BMC_design.xlsx')
print(reader.adc_par)