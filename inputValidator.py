from pathlib import Path
import PySimpleGUI as sg
import os.path

def ValidateInput(values) -> tuple:
    '''Returns tuple (success, extraction_type)'''
    inValidList = []
    isValid = True
    for value in values:
        if type(value) == int:
            print(f"{value} is of type int")
            continue
        elif value == "-SERIAL_PORT-":
            response = ValidateSPComboBox(value)
            if not response:
                inValidList.append("Serial Port")
                isValid = False
        elif value == "-HOST_IP_INPUT-":
            pass
        elif (value == "-IMAGE-" or value == "-EMBEDED_SRC-" or 
                value == "-FARMSERVER-" or value == "-FARMSERVERF1INSTALLER-" or
                value == "-DB_FILE-" or value == "-NAND_SRC_PATH-" or value == "-DB_FILE_SRC-"):
            response = CheckValidFilePath(values, value)
            if not response[0]:
                inValidList.append(value)
                isValid = False

        elif value == "-IMPORTDB-":
            pass
        elif value == "-SN-":
            pass
        elif value == "-TO_RTS-":
            pass
        elif value == "-FROM_RTS-":
            pass
        elif value == "-SOM_DESIRED_IP-":
            pass
        elif value == "-SOM_DESIRED_IP-":
            pass
        else:
            print(value)
            pass
    
    if len(inValidList) > 0:
        mapInputs = {
            '-IMAGE-': 'Image Path',
            '-EMBEDED_SRC-': 'Embedded_src_Path',
            '-FARMSERVER-': 'farmserverfillsrc',
            '-FARMSERVERF1INSTALLER-': 'farserverf1installersrc',
            '-DB_FILE-': 'pathtodbfile',
            '-NAND_SRC_PATH-': 'nand_src_path',
            '-DB_FILE_SRC-': 'dbfilesrc',
        }
        invalidMarkups = []
        for value in inValidList:
            invalidMarkups.append(mapInputs[value])
        
        sg.PopupError(f'Incorrect INPUT file/files for the following Catagories!\n {invalidMarkups}')

def CheckValidFilePath(values, value):
    i_path = values[value]
    if i_path == '':
        pass
    if len(i_path) == 0:
        #sg.PopupError('No INPUT file or folder selected!')
        return False, value
    elif not os.path.exists(i_path):
        #sg.PopupError('INPUT file/folder does not exist!')
        return False, value
    elif os.path.isdir(i_path):
        ext_type = 'fs'
    else: # must be an existing file then
        if i_path.lower().endswith('.tar') and not i_path.lower().endswith('.zip'):
            #sg.PopupError('Input file is not a supported archive! ', i_path)
            return False, value
        else:
            ext_type = Path(i_path).suffix[1:].lower() 
            return True, ext_type


def ValidateSPComboBox(value):
    if (len(value) != 0):
        is_valid = True
    else:
        is_valid = False
    return is_valid, 