from pathlib import Path
import PySimpleGUI as sg
import os.path


def ValidateInputs(values) -> tuple:
    '''Returns tuple (success, extraction_type)'''
    inValidList = []
    isValid = True
    for value in values:
        if 'BROWSE' in value.upper():
            print(value)
        else:
            if (value == "-SERIAL_PORT-" or  value == "-HOST_IP_INPUT-"
                    or value == "-SN-" or value == "-TO_RTS-" or value == "-FROM_RTS-"):
                response = ValidateInput(value)
                if not response[0]:
                    inValidList.append(value)
                    isValid = False

            elif (value == "-IMAGE-" or value == "-EMBEDED_SRC-" or 
                    value == "-FARMSERVER-" or value == "-FARMSERVERF1INSTALLER-" or
                    value == "-DB_FILE-" or value == "-NAND_SRC_PATH-" or value == "-DB_FILE_SRC-"):
                response = CheckValidFilePath(values, value)
                if not response[0]:
                    inValidList.append(value)
                    isValid = False

            elif value == "-SOM_DESIRED_IP-":
                pass
            elif value == "-F1_UNIT-":
                pass
            else:
                if value == "-IMPORTDBBOOL-":
                    if values[value] == False:
                        pass
                    else:
                        value = "-IMPORTDB-"
                        response = CheckValidFilePath(values, value)
                        if not response[0]:
                            inValidList.append(value)
                            isValid = False

    ThrowPopUpError(inValidList)



def ThrowPopUpError(inValidList):
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
                '-TO_RTS-': 'To_RTS_PORT',
                '-FROM_RTS-': 'FROM_RTS_PORT',
                '-SOM_DESIRED_IP-': 'SOM_DESIRED_IP',
                '-F1_UNIT-': 'F1_UNIT_PREP_FINAL_IP_CONFIGS',
            }
        invalidMarkups = []
        for value in inValidList:
            invalidMarkups.append(mapInputs[value])
        
        sg.PopupError(f'Incorrect INPUT file/files for the following Catagories!\n {printError(invalidMarkups)}')

def printError(errors):
    str = ''
    for error in errors:
        str += f"\n- {error}"
    return str


def CheckValidFilePath(values, value):
    path = values[value]
    if type(path) == bool:
        pass
    elif len(path) == 0 or path == '':
        return False, value
    elif not os.path.exists(path):
        return False, value
    elif os.path.isdir(path):
        ext_type = 'fs'
        return False, ext_type
    else:
        #is image path
        if (path.lower().endswith('.jpeg') or path.lower().endswith('.png')
            or path.lower().endswith('.png') or path.lower().endswith('.webp') 
            or path.lower().endswith('.svg') or path.lower().endswith('.gz')):
            return True, path
        #is embedded_src_path, nand_src_path
        elif (path.lower().endswith('.gz') or path.lower().endswith('.bin')):
            return True, path
        #is database path
        elif (path.lower().endswith('.sql') or path.lower().endswith('.json')):
            return True, path
        #is farmerserver path
        elif (path.lower().endswith('.jar') or path.lower().endswith('.sh')):
            return True, path
        else:
            ext_type = Path(path).suffix[1:].lower() 
            return True, ext_type


def ValidateInput(value):
    if (len(value) != 0):
        is_valid = True
    else:
        is_valid = False
    return is_valid, value