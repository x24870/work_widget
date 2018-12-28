import openpyxl

FILE_NAME = 'BMC_design.xlsx'
SHEET_NAME = 'GPIO Table'

def read_sheet(file_name, sheet_name):
    gpio_table = []

    wb = openpyxl.load_workbook(file_name, read_only=True)
    sheet_names = wb.get_sheet_names()
    if sheet_name not in sheet_names:
        print("Can't find '{}' in '{}'".format(file_name, sheet_name))
        return
    sheet = wb.get_sheet_by_name(sheet_name)

    
    row_start = 7
    row_end = 235
    #GPIO cell column
    GPIO_col = 'B'
    #Current Application cell column
    CA_col = 'E' 
    #Signal DirectiO, P/Pn cell column
    SD_col = 'M'
    for i in range(row_start, row_end):
        if sheet[CA_col + str(i)].value == 'GPIO' and sheet[SD_col + str(i)].value:
            #pin_def format [pin, io, status] 
            pin_def = []
            pin_def.append(sheet[GPIO_col + str(i)].value)
            pin_def.append(sheet[SD_col + str(i)].value)
            pin_def.append(0)#!!!set all pin to low for test!!!
            gpio_table.append(pin_def)

    for i in gpio_table:
        print(i)

    return gpio_table

def get_str(pin, io, status):
    #group_str = '/* GPIO Group {} */'
    ret_str = []
    if io == 'Input':
        ret_str.append('set_gpio_dir_input({});//Input'.format(pin))
    elif io == 'Output O.D.':
        ret_str.append('set_gpio_dir_input({});//Output O.D.'.format(pin))
    else:
        ret_str.append('set_gpio_dir_output({});//Output-PushPull'.format(pin))
        if status == 1:
            ret_str.append('set_gpio_data_high({});//Output-PushPull'.format(pin))
        else:
            ret_str.append('set_gpio_data_low({});'.format(pin))

    return ret_str
    

def gen_file_predix(file_name):
    predix = '''#include <stdio.h>
#include <stdlib.h>
#include "gpioset.h"
#include "gpioifc.h"

void GPIOInit(void)
{
    printf("Pegatron Gpio Init start \\n");
'''
    with open(file_name, 'w') as f:
        f.write(predix)

def gen_file_suffix(file_name):
    suffix = '''
    printf("Pegatron Gpio Init END \\n");

    return ;
}
    '''
    with open(file_name, 'a') as f:
        f.write(suffix)

def specify_group(pin):
    group = pin.split('GPIO')[1]
    for char in group:
        if char.isdigit():
            group  = group.split(char)[0]
    return(group)

def gen_file(gpio_table):
    file_name = 'gpioset.c'
    gen_file_predix(file_name)

    with open(file_name, 'a') as f:
        group = None
        for pin_def in gpio_table:
            if group != specify_group(pin_def[0]):
                group = specify_group(pin_def[0])
                f.write('\n    /* GPIO Group {} */\n'.format(group))

            for pin_str in get_str(pin_def[0], pin_def[1], pin_def[2]):
                f.write('    ' + pin_str + '\n')
            
    gen_file_suffix(file_name)

if __name__ == '__main__':
    test_gpio_table = [
        ['GPIOA0', 'Output O.D.', 0], 
        ['GPIOB1', 'Output-PushPull', 0], 
        ['GPIOAA1', 'Output-PushPull', 1], 
        ['GPIOAB1', 'Input', 0]
    ]

    gpio_table = read_sheet(FILE_NAME, SHEET_NAME)
    gen_file(gpio_table)