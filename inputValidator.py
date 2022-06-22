from pathlib import Path
import ipaddress
import PySimpleGUI as sg
import os.path
import serial.tools.list_ports

row1Validations = []
row2Validations =[]

def ValidateRow1Inputs(values, window) -> list:
    global row1Validations
    row1Validations.clear()
    '''Returns list of invalid inputs from window'''
    for value in values:
        if 'BROWSE' in value.upper():
            pass
        else:
            if value == "-HOST_IP_INPUT-" or value == "-SERIAL_PORT-":
                Validaterow1Input(value, values)

            elif (value == "-IMAGE-" or value == "-EMBEDED_SRC-" or 
                    value == "-FARMSERVER-" or value == "-FARMSERVERF1INSTALLER-" or
                    value == "-DB_FILE-" or value == "-NAND_SRC_PATH-" or value == "-DB_FILE_SRC-"):
                
                CheckValidFilePath(values, value)

            else:
                if value == "-IMPORTDBBOOL-":
                    if values[value]:
                        value = "-IMPORTDB-"
                        CheckValidFilePath(values, value)
    if len(row1Validations) > 0:
        ThrowPopUpError(window)
    
    return row1Validations


def ThrowPopUpError(window):
    global row1Validations
    global row2Validations
    invalidMarkups = []

    mapInputs = {
        '-IMAGE-': 'Image Path',
        '-EMBEDED_SRC-': 'Embedded_src_Path',
        '-FARMSERVER-': 'farmserverfillsrc',
        '-FARMSERVERF1INSTALLER-': 'farserverf1installersrc',
        '-DB_FILE-': 'pathtodbfile',
        "-IMPORTDB-": 'Import Database',
        "-DB_FILE_SRC-": "Db File Source",
        '-NAND_SRC_PATH-': 'nand_src_path',
        '-SERIAL_PORT-': 'Serial Port',
        '-HOST_IP_INPUT-': 'Host_Ip',
        '-SN-': 'Serial Number',
        '-TO_RTS-': 'to_rts_port',
        '-FROM_RTS-': 'from_rts_port',
        '-SOM_DESIRED_IP-': 'som_desired_ip',
        '-F1_UNIT-': 'F1_UNIT_PREP_FINAL_IP_CONFIGS',
    }
    [invalidMarkups.append(mapInputs[x]) for x in row1Validations]
    if len(row2Validations) > 0:
        [invalidMarkups.append(mapInputs[x]) for x in row2Validations]

    sg.PopupError(f'Incorrect INPUT file / files for the following Catagories!\n {printError(invalidMarkups)}')


def printError(errors):
    str = ''
    for error in errors:
        str += f"\n- {error}"
    return str


def CheckValidFilePath(values, value):
    path = values[value]
    global row1Validations

    if type(path) == bool:
        row1Validations.append(value)
    elif len(path) == 0 or path == '':
        row1Validations.append(value)
    elif os.path.isdir(path):
        row1Validations.append(value)

    elif not os.path.exists(path): 
        row1Validations.append(value)
    else:
        file_extension = os.path.splitext(path)[1]
        if file_extension == '':
            row1Validations.append(value)


def Validaterow2Input(value, values):
    global row2Validations
    v = values[value]
    if len(v) <= 0 or v == '':
        row2Validations.append(value)


def Validaterow1Input(value, values):
    global row2Validations
    v = values[value]
    if len(v) <= 0 or v == '':
        row1Validations.append(value)


def ValidatePortLength(value, values):
    global row2Validations
    v = values[value]
    if len(v) != 4:
        row2Validations.append(value)


def validate_ip_address(value, values):
    global row2Validations
    add = values[value]
    try:
        ip = ipaddress.ip_address(add)
    except:
        row2Validations.append(value)

#---------------row two elements for validation-------------------------]
def ValidateAllInputs(values, window) -> tuple:
    '''returns a tuple, first value being a boolean statement, and the second a list of invalid input elements'''
    global row2Validations
    row2Validations.clear()
    isValid = False
    for value in values:
        if value == "-SN-":
            Validaterow2Input(value, values)
        elif value == "-TO_RTS-" or value == '-FROM_RTS-':
            ValidatePortLength(value, values)
        elif value == "-SOM_DESIRED_IP-":
            validate_ip_address(value, values)
        elif value == '-F1_UNIT-':
            v = values[value]
            if v == 'Static':
                DHCP = False
            elif v == 'DHCP':
                DHCP = True
            else:
                row2Validations.append(value)
    row1Validations = ValidateRow1Inputs(values, window)
    allInputList = row1Validations + row2Validations
    allInputList.sort()

    if len(allInputList) == 0:
        isValid = True
    return (isValid, allInputList)


def updateStatusBar(progress_bar, i):
    progress_bar.UpdateBar(i + 50)
    i += 50
    return i, progress_bar


def HighlightIncorrectInputs(values, errors, window):
    valuesList = []

    for value in values.keys():
        if 'BROWSE' in value.upper():
            pass
        else:
            valuesList.append(value)
    if len(valuesList) > 0:
        valuesList.sort()
        
    for error in errors:
        if not error == "-SERIAL_PORT-" and not error == "-F1_UNIT-" and not error == '-IMPORTDBBOOL-':
            window[f'{error}'].Update(background_color = "red")
        if error in valuesList:
            valuesList.remove(error)
    for value in valuesList:
        if not value == "-SERIAL_PORT-" and not value == "-F1_UNIT-" and not value == '-IMPORTDBBOOL-':
            window[f'{value}'].Update(background_color = "white")