import openpyxl

class sheetReader():
    def __init__ (self):
        self.adc_par = {}

    def read_bmc_design_sheet(self, filename):
        wb = None
        try:
            wb = openpyxl.load_workbook(filename, read_only=True, data_only=True)
        except:
            print("Error: Can't find {}".format(filename))

        if wb:
            self._get_adc_par(wb)

        return

    def _get_adc_par(self, wb):
        sheet_name = 'ADC'
        if sheet_name not in wb.get_sheet_names():
            print("Can't find ADC page")
            return
        sheet = wb.get_sheet_by_name(sheet_name)

        start_row = 2
        sensor_name_col = 'A'
        lowNR_col = 'F'
        lowCri_col = 'G'
        lowWarn_col = 'H'
        HighWarn_col = 'J'
        HighCri_col = 'K'
        HighNR_col = 'L'
        M_col = 'M'
        R1_col = 'W'
        R2_col = 'X'

        for i in range(start_row, 18):
            sensor_name = sheet[sensor_name_col + str(i)].value
            if sensor_name:
                dict_ = self.adc_par[sensor_name] = {}
                dict_['lowNR'] = sheet[lowNR_col + str(i)].value
                dict_['lowCri'] = sheet[lowCri_col + str(i)].value
                dict_['lowWarn'] = sheet[lowWarn_col + str(i)].value
                dict_['HighWarn'] = sheet[HighWarn_col + str(i)].value
                dict_['HighCri'] = sheet[HighCri_col + str(i)].value
                dict_['HighNR'] = sheet[HighNR_col + str(i)].value
                dict_['M'] = sheet[M_col + str(i)].value
                dict_['R1'] = sheet[R1_col + str(i)].value
                dict_['R2'] = sheet[R2_col + str(i)].value

                #print(self.adc_par[sensor_name])
        

if __name__ == "__main__":
    reader = sheetReader()
    reader.read_bmc_design_sheet('BMC_design.xlsx')