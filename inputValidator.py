from pathlib import Path
import ipaddress
import PySimpleGUI as sg
import os.path
import serial.tools.list_ports

inValidList = []
isValid = True

def ValidateRow1Inputs(values, window):
    '''Returns tuple (success, extraction_type)'''
    for value in values:
        if 'BROWSE' in value.upper():
            #print(value)
            pass
        else:
            if value == "-HOST_IP_INPUT-" or value == "-SERIAL_PORT-":
                if value == '-SERIAL_PORT-':
                    pass

                ValidateInput(value, values)

            elif (value == "-IMAGE-" or value == "-EMBEDED_SRC-" or 
                    value == "-FARMSERVER-" or value == "-FARMSERVERF1INSTALLER-" or
                    value == "-DB_FILE-" or value == "-NAND_SRC_PATH-" or value == "-DB_FILE_SRC-"):
                
                CheckValidFilePath(values, value)

            else:
                if value == "-IMPORTDBBOOL-":
                    if values[value]:
                        value = "-IMPORTDB-"
                        CheckValidFilePath(values, value)

    ThrowPopUpError(inValidList, window)


def ThrowPopUpError(inValidList, window):
    window.read(timeout=100)
    invalidMarkups = []

    if len(inValidList) > 0:
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
    for value in inValidList:
        invalidMarkups.append(mapInputs[value])
    
    sg.PopupError(f'Incorrect INPUT file / files for the following Catagories!\n {printError(invalidMarkups)}')
    inValidList.clear()
    invalidMarkups.clear()

def printError(errors):
    str = ''
    for error in errors:
        str += f"\n- {error}"
    return str


def CheckValidFilePath(values, value):
    path = values[value]
    global isValid

    if type(path) == bool:
        inValidList.append(value)
        isValid = False
    elif len(path) == 0 or path == '':
        inValidList.append(value)
        isValid = False
    elif os.path.isdir(path):
        inValidList.append(value)
        isValid = False

    elif not os.path.exists(path): 
        inValidList.append(value)
        isValid = False
    else:
        file_extension = os.path.splitext(path)[1]
        if file_extension == '':
            inValidList.append(value)
            isValid = False
        




def ValidateInput(value, values):
    global isValid
    v = values[value]
    if len(v) <= 0 or v == '':
        inValidList.append(value)
        isValid = False

def ValidatePortLength(value, values):
    global isValid
    v = values[value]
    if len(v) != 4:
        inValidList.append(value)
        isValid = False

def validate_ip_address(value, values):
    global isValid
    add = values[value]
    try:
        ip = ipaddress.ip_address(add)
        print("IP address {} is valid. The object returned is {}".format(add, ip))
    except:
        inValidList.append(value)
        isValid = False

#---------------row two elements for validation-------------------------]
def ValidateAllInputs(values, window):
    global isValid
    for value in values:
        if value == "-SN-":
            ValidateInput(value, values)
        elif value == "-TO_RTS-" or value == '-FROM_RTS-':
            ValidatePortLength(value, values)
        elif value == "-SOM_DESIRED_IP-":
            validate_ip_address(value, values)
        elif value == '-F1_UNIT-':
            v = values[value]
            print(v)
            if v == 'Static':
                Static = True
            elif v == 'DHCP':
                DHCP = True
            else:
                inValidList.append(value)
                isValid = False

    
    ValidateRow1Inputs(values, window)

    return isValid



def updateStatusBar(progress_bar, i):
    progress_bar.UpdateBar(i + 50)
    i += 50
    return i, progress_bar