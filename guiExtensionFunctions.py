import ipaddress
import PySimpleGUI as sg
import os.path

invalid_inputs = []
mapValidInputValues = {}
mapInputs = {
        '-IMAGE-': 'Image Path',
        '-EMBEDED_SRC-': 'Embedded_src_Path',
        '-FARMSERVER-': 'farmserverfillsrc',
        '-FARMSERVERF1INSTALLER-': 'farserverf1installersrc',
        '-DB_FILE-': 'pathtodbfile',
        "-IMPORTDB-": 'Import Database',
        "-IMPORTDBBOOL-": "Data Import Checkbox",
        "-DB_FILE_SRC-": "Db File Source",
        '-NAND_SRC_PATH-': 'nand_src_path',
        '-SERIAL_PORT-': 'Serial Port',
        '-HOST_IP_INPUT-': 'Host_Ip',
        '-SN-': 'Serial Number',
        '-TO_RTS-': 'to_rts_port',
        '-FROM_RTS-': 'from_rts_port',
        '-SOM_DESIRED_IP-': 'som_desired_ip',
        '-DHCP-': 'F1_UNIT_PREP_FINAL_IP_CONFIGS',
    }


def ThrowPopUpError():
    invalidMarkups = []

    [invalidMarkups.append(mapInputs[x]) for x in invalid_inputs]

    sg.PopupError(f'Incorrect File or Files for the following Catagories!\n {printError(invalidMarkups)}')


def validfile(path, forced_ext='') -> bool:
    if not os.path.exists(path): 
        return False
    if forced_ext > '':
        file_extension = os.path.splitext(path)[1]
        if file_extension != forced_ext:
            return False
    return True


def printError(errors) -> str:
    str = ''
    for error in errors:
        str += f"\n- {error}"
    return str


def CheckValidFilePath(values, value):
    path = values[value]
    global invalid_inputs
    global mapValidInputValues

    file_exten_value = True
    file_exten_value = validfile(path, forced_ext='.txt') #FOR DEV PURPOSES. IN POST DEV COMMENT LINE 57 AND RETURN 61-72
    #ALL FILES SAVED AS TXT. 
    #IN NON DEVELOPMENT ENVIROMENT UNBLOCK COMMENTED CODE
    #---------------------------------------------------
    # if value == '-IMAGE-' or value == "-EMBEDED_SRC-":
    #     file_exten_value = validfile(path, forced_ext='.gz')
    # elif value == "-FARMSERVER-":
    #     file_exten_value = validfile(path, forced_ext='.jar')
    # elif value == "-FARMSERVERF1INSTALLER-":
    #     file_exten_value = validfile(path, forced_ext='.sh')
    # elif value == "-DB_FILE-" or value == "-DB_FILE_SRC-" or value == "-IMPORTDB-":
    #     file_exten_value = validfile(path, forced_ext='.sql')
    #     if not file_exten_value:
    #         file_exten_value = validfile(path, forced_ext='.json')
    # elif value == "-NAND_SRC_PATH-":
    #     file_exten_value = validfile(path, forced_ext='.bin')
    #---------------------------------------------------
    if not file_exten_value:
        invalid_inputs.append(value)
    else:
        mapValidInputValues[mapInputs[value]] = path, value

def ValidateInput(value, values):
    global invalid_inputs
    global mapValidInputValues
    v = values[value]
    if len(v) <= 0 or v == '':
        invalid_inputs.append(value)
    else:
        mapValidInputValues[mapInputs[value]] = v, value


def ValidatePortLength(value, values):
    global invalid_inputs
    global mapValidInputValues
    v = values[value]
    if len(v) != 4:
        invalid_inputs.append(value)
    else:
        mapValidInputValues[mapInputs[value]] = v, value


def validate_ip_address(value, values):
    global invalid_inputs
    global mapValidInputValues
    address = values[value]
    try:
        ipaddress.ip_address(address)
        mapValidInputValues[mapInputs[value]] = address, value
    except:
        invalid_inputs.append(value)


def HighlightIncorrectInputs(values, errors, window):
    valuesList = []
    global invalid_inputs
    for value in values.keys():
        if 'BROWSE' in value.upper():
            pass
        else:
            valuesList.append(value)
    valuesList.sort()
    if len(invalid_inputs) > 0:
        for error in invalid_inputs:
            if not invalid_inputs == "-SERIAL_PORT-" and not invalid_inputs == "-DHCP-" and not invalid_inputs == '-IMPORTDBBOOL-':
                window[f'{error}'](background_color = "red")

            if error in valuesList:
                valuesList.remove(error)
        ThrowPopUpError()

    for value in valuesList:
        if not value == "-SERIAL_PORT-" and not value == "-DHCP-" and not value == '-IMPORTDBBOOL-':
            window[f'{value}'](background_color = "white")


def ValidateAllInputs(values,window) -> tuple:
    '''
    returns a boolean statement, a list of invalid input elements,
    and  a list of valid input elements'''
    global invalid_inputs
    global mapValidInputValues
    invalid_inputs.clear()
    isValid = False #Set to true to run development without inputs
    for value in values:
        if value == "-SN-" or value == "-SERIAL_PORT-":
            ValidateInput(value, values)
        elif value == "-TO_RTS-" or value == '-FROM_RTS-':
            ValidatePortLength(value, values)
        elif value == "-SOM_DESIRED_IP-" or  value == "-HOST_IP_INPUT-":
            validate_ip_address(value, values)
        elif value == '-DHCP-':
            v = values[value]
            if v == 'Static':
                mapValidInputValues[mapInputs[value]] = v, value
            elif v == 'DHCP':
                mapValidInputValues[mapInputs[value]] = v, value
            else:
                invalid_inputs.append(value)
        elif (value == "-IMAGE-" or value == "-EMBEDED_SRC-" or 
                value == "-FARMSERVER-" or value == "-FARMSERVERF1INSTALLER-" or
                value == "-DB_FILE-" or value == "-NAND_SRC_PATH-" or value == "-DB_FILE_SRC-"):
            
            CheckValidFilePath(values, value)
        elif value == "-IMPORTDBBOOL-":
            db_bool = values[value]
            if db_bool:
                mapValidInputValues[mapInputs[value]] = db_bool, value
                value = "-IMPORTDB-"
                CheckValidFilePath(values, value)
            else:
                mapValidInputValues[mapInputs[value]],mapValidInputValues[mapInputs["-IMPORTDB-"]] = (db_bool, value), ("", value)

    if len(invalid_inputs) == 0:
        isValid = True
    return isValid, invalid_inputs, mapValidInputValues.keys()


