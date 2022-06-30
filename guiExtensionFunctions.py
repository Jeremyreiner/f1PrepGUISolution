from ast import Not
import ipaddress
import PySimpleGUI as sg
import os.path

invalid_inputs = []
red_inputs = set()
mapValidInputValues = {}
map_inputs = {
        '-IMAGE-': 'Image Path',
        '-EMBEDED_SRC-': 'Embedded_src_Path',
        '-FARMSERVER-': 'farmserverfillsrc',
        '-FARMSERVERF1INSTALLER-': 'farserverf1installersrc',
        '-DB_FILE-': 'pathtodbfile',
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


def JsonToGuiKeys(key):
    if key in map_inputs.values():
        for k,v in map_inputs.items():
            if v == key:
                return k
    


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
        str += f"\n- {map_inputs[error]}"
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
    # elif value == "-DB_FILE-" or value == "-DB_FILE_SRC-":
    #     file_exten_value = validfile(path, forced_ext='.sql')
    #     if not file_exten_value:
    #         file_exten_value = validfile(path, forced_ext='.json')
    # elif value == "-NAND_SRC_PATH-":
    #     file_exten_value = validfile(path, forced_ext='.bin')
    #---------------------------------------------------
    if not file_exten_value:
        invalid_inputs.append(value)
    else:
        mapValidInputValues[map_inputs[value]] = path


def ValidateInput(value, values):
    global invalid_inputs
    global mapValidInputValues
    v = values[value]
    if len(v) <= 0 or v == '':
        invalid_inputs.append(value)
    else:
        mapValidInputValues[map_inputs[value]] = v


def ValidatePortLength(value, values):
    global invalid_inputs
    global mapValidInputValues
    v = values[value]
    if v=="" or int(v) < 1000 or int(v) > 6500:
        invalid_inputs.append(value)
    else:
        mapValidInputValues[map_inputs[value]] = v


def validate_ip_address(value, values):
    global invalid_inputs
    global mapValidInputValues
    address = values[value]
    try:
        ipaddress.ip_address(address)
        mapValidInputValues[map_inputs[value]] = address
    except:
        invalid_inputs.append(value)

def FixHighlightedInputs(window):
    global red_inputs
    if len(red_inputs) > 0:
        for value in red_inputs:
            if value not in invalid_inputs:
                window[f'{value}'](background_color = "white")
            


def HighlightIncorrectInputs(window):
    flag = False
    if len(invalid_inputs) > 0:
        for error in invalid_inputs:
            if not error == "-SERIAL_PORT-" and not error == "-DHCP-" and not error == '-IMPORTDBBOOL-':
                window[f'{error}'](background_color = "red")
                red_inputs.add(error)
        for error in invalid_inputs:
            if not (error == "-SN-" or error == "-TO_RTS-" or
                    error == "-FROM_RTS-" or error == "-DHCP-"
                    or error == "-SOM_DESIRED_IP-"):
                    flag = True
                    break
    input = "INPUTS" if len(invalid_inputs) > 1 else "INPUT"
    if flag:
        sg.PopupError(f'INCORRECT/ MISSING {input} IN THE FOLLOWING CATAGORIES!\n {printError(invalid_inputs)}')
    else:
        sg.PopupError(f'SETTINGS HAVE BEEN SAVED, TO RUN THE PROGRAM THE FOLLOWING {input} MUST BE CORRECTED\n {printError(invalid_inputs)}')


def ValidateAllInputs(values,window) -> tuple:
    '''
    returns a boolean statement, a list of invalid input elements,
    and  a list of valid input elements'''
    global invalid_inputs
    global mapValidInputValues
    invalid_inputs.clear()
    isValid = False #Set true to run development without inputs
    for value in values:
        if value == "-SN-":
            ValidateInput(value, values)
        elif value == "-TO_RTS-" or value == '-FROM_RTS-':
            ValidatePortLength(value, values)
        elif value == "-SOM_DESIRED_IP-" or  value == "-HOST_IP_INPUT-":
            validate_ip_address(value, values)
        elif value == '-DHCP-':
            v = values[value]
            if v == 'Static':
                mapValidInputValues[map_inputs[value]] = v
            elif v == 'DHCP':
                mapValidInputValues[map_inputs[value]] = v
            else:
                invalid_inputs.append(value)
        elif (value == "-IMAGE-" or value == "-EMBEDED_SRC-" or 
                value == "-FARMSERVER-" or value == "-FARMSERVERF1INSTALLER-" or
                value == "-DB_FILE-" or value == "-NAND_SRC_PATH-" or value == "-DB_FILE_SRC-"):
            
            CheckValidFilePath(values, value)
        elif value == "-IMPORTDBBOOL-":
            db_bool = values[value]
            if db_bool:
                mapValidInputValues[map_inputs[value]] = db_bool
            else:
                mapValidInputValues[map_inputs[value]] = db_bool
    if len(invalid_inputs) == 0:
        isValid = True
    else:
        HighlightIncorrectInputs(window)
    FixHighlightedInputs(window)

    return isValid, mapValidInputValues.keys()


