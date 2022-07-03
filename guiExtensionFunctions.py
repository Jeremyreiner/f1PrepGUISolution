import ipaddress
import os.path
import re

invalid_inputs = set()
map_valid_input_values = {} #[Key] is map_inputs value for a more readable name, [Value] input enterred from given gui field #used to calculate progress bar
map_inputs = {
        '-IMAGE-': 'image_path',
        '-EMBEDED_SRC-': 'embedded_src_path',
        '-FARMSERVER-': 'farmserverfilesrc',
        '-FARMSERVERF1INSTALLER-': 'farmserverf1installersrc',
        '-DB_FILE-': 'PathToDBfile',
        "-IMPORTDBBOOL-": "importdatabase",
        "-DB_FILE_SRC-": "dbfilesrc",
        '-NAND_SRC_PATH-': 'nand_src_path',
        '-SERIAL_PORT-': 'Serial Port',
        '-HOST_IP_INPUT-': 'host_ip',
        '-SN-': 'serial_number',
        '-TO_RTS-': 'TO_RTS_PORT',
        '-FROM_RTS-': 'FROM_RTS_PORT',
        '-SOM_DESIRED_IP-': 'som_desired_ip',
        '-DHCP-': 'f1_unit_prep_final_ip_config',
    }

v_to_g = {}
for v in map_inputs:
    v_to_g[map_inputs[v]]=v


def validfile(path: str, forced_ext='') -> bool:
    if not os.path.exists(path): 
        return False
    if forced_ext > '':
        file_extension = os.path.splitext(path)[1]
        if file_extension != forced_ext:
            return False
    return True


def printError(errors: list) -> str:
    str = ''
    for error in errors:
        str += f"\n- {map_inputs[error]}"
    return str


def CheckValidFilePath(path: str, value: str):
    global invalid_inputs
    global map_valid_input_values

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
    # elif value == "-DB_FILE-" or value == "-DB_FILE_SRC-":invalid_inputs.add
    #     file_exten_value = validfile(path, forced_ext='.sql')
    #     if not file_exten_value:
    #         file_exten_value = validfile(path, forced_ext='.json')
    # elif value == "-NAND_SRC_PATH-":
    #     file_exten_value = validfile(path, forced_ext='.bin')
    #---------------------------------------------------
    if not file_exten_value:
        invalid_inputs.add(value)
    else:
        map_valid_input_values[map_inputs[value]] = path


def ValidateInput(value:str, path:str):
    global invalid_inputs
    global map_valid_input_values
    letters = bool(re.match(r'\w*[A-Z]\w', path))
    numbers = bool(re.match(r'\w*[1-9]\w', path))
    symbols = any(not x.isalnum() for x in path)

    if letters and numbers and not symbols:
        map_valid_input_values[map_inputs[value]] = path
    else:
        invalid_inputs.add(value)


def ValidatePortLength(value:str, path:str):
    global invalid_inputs
    global map_valid_input_values
    if path=="" or int(path) < 1000 or int(path) > 6553:
        invalid_inputs.add(value)
    else:
        map_valid_input_values[map_inputs[value]] = path


def ValidateIpAddress(value:str, path:str):
    global invalid_inputs
    global map_valid_input_values
    try:
        ipaddress.ip_address(path)
        map_valid_input_values[map_inputs[value]] = path
    except:
        invalid_inputs.add(value)


def ValidateSettings(invalid_inputs: set) -> set:
    settings = set()
    for field in invalid_inputs:
        if not (field == "-SN-" or field == "-TO_RTS-" or
                    field == "-FROM_RTS-" or field == "-DHCP-"
                    or field == "-SOM_DESIRED_IP-"):
            settings.add(field)
    return settings


def ValidateAllInputs(values: dict) -> tuple:
    '''
    returns a boolean statement, interval rate for progression bar'''
    global invalid_inputs
    global map_valid_input_values
    invalid_inputs.clear()
    isValid = False #Set true to run development without inputs
    for value in values:
        path=values[value]
        if value == "-SN-":
            ValidateInput(value, path)
        elif value == "-TO_RTS-" or value == '-FROM_RTS-':
            ValidatePortLength(value, path)
        elif value == "-SOM_DESIRED_IP-" or  value == "-HOST_IP_INPUT-":
            ValidateIpAddress(value, path)
        elif value == '-DHCP-':
            v = values[value]
            if v == 'Static':
                map_valid_input_values[map_inputs[value]] = v
            elif v == 'DHCP':
                map_valid_input_values[map_inputs[value]] = v
            else:
                invalid_inputs.add(value)
        elif (value == "-IMAGE-" or value == "-EMBEDED_SRC-" or 
                value == "-FARMSERVER-" or value == "-FARMSERVERF1INSTALLER-" or
                value == "-DB_FILE-" or value == "-NAND_SRC_PATH-" or value == "-DB_FILE_SRC-"):
            
            CheckValidFilePath(path, value)
        elif value == "-IMPORTDBBOOL-":
            db_bool = values[value]
            if db_bool:
                map_valid_input_values[map_inputs[value]] = db_bool
            else:
                map_valid_input_values[map_inputs[value]] = db_bool
    if len(invalid_inputs) == 0:
        isValid = True
        interval = int(100/len(map_valid_input_values.keys()))
        return isValid, interval
    else:
        return isValid, 0