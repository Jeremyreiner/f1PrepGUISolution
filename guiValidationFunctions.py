import ipaddress
import os.path as op
import re
from string import ascii_letters, digits

invalid_inputs = set()
map_valid_input_values = {} #[Key] is map_inputs key for a more readable name, [Value] input enterred from given gui field #used in mockscript
map_inputs = {
        '-IMAGE-': 'image_path',
        '-EMBEDED_SRC-': 'embedded_src_path',
        '-FARMSERVER-': 'farmserverfilesrc',
        '-FARMSERVERF1INSTALLER-': 'farmserverf1installersrc',
        '-DB_FILE-': 'PathToDBfile',
        "-IMPORTDBBOOL-": "importdatabase",
        "-DB_FILE_SRC-": "dbfilesrc",
        '-NAND_SRC_PATH-': 'nand_src_path',
        '-SERIAL_PORT-': 'port',
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


def validfile(value: str, forced_ext='') -> bool:
    if not op.exists(value): 
        return False
    if forced_ext > '':
        file_extension = op.splitext(value)[1]
        if file_extension != forced_ext:
            return False
    return True


def printError(errors: list) -> str:
    str = ''
    for error in errors:
        str += f"\n- {map_inputs[error]}"
    return str


def CheckValidFilePath(value: str, key:str) -> bool:
    '''
    Checks input paths, identifying 
    A: if the path is a located on the current device,
    B: If the current path is ending with the correct extension 
    '''
    keyMap = {
        "-IMAGE-": ".gz",
        "-EMBEDED_SRC-": ".gz",
        "-FARMSERVER-": ".jar",
        "-FARMSERVERF1INSTALLER-": ".sh",
        "-DB_FILE-": ".sql",
        "-DB_FILE_SRC-": ".sql",
        "-NAND_SRC_PATH-": ".bin",
    }
    if key in keyMap:
        file_exten_value = validfile(value, forced_ext=keyMap[key])
    
    file_exten_value = validfile(value, forced_ext='.txt') ##TODO Block this line 
    if not file_exten_value:
        return False
    return True


def SettingsRow(invalid_inputs: set) -> set:
    '''
    Takes in all invalid inputs enterred and returns a set of the elements
    from only the settings row'''
    settings = set()
    for field in invalid_inputs:
        if not (field == "-SN-" or field == "-TO_RTS-" or
                    field == "-FROM_RTS-" or field == "-DHCP-"
                    or field == "-SOM_DESIRED_IP-"):
            settings.add(field)
    return settings


def ValidateAllInputs(values: dict) -> bool:
    '''
    Main validation function checks all inputs from the gui, and returns a 
    boolean response of true if all the inputs have succesfully been validated,
    or false if there was any incorrect inputs enterred'''
    global invalid_inputs
    global map_valid_input_values
    invalid_inputs.clear()
    isValid = False #Set true to run development without inputs
    for key in values:
        value=values[key]
        if key == "-SN-":
            if not set(value).difference(ascii_letters.upper() + digits):
                map_valid_input_values[map_inputs[key]] = values[key]
            else:
                invalid_inputs.add(key)

        elif key == "-TO_RTS-" or key == '-FROM_RTS-':
            if value=="" or int(value) < 1000 or int(value) > 6553:
                invalid_inputs.add(key)
            else:
                map_valid_input_values[map_inputs[key]] = values[key]

        elif key == "-SOM_DESIRED_IP-" or  key == "-HOST_IP_INPUT-":
            try:
                ipaddress.ip_address(value)
                map_valid_input_values[map_inputs[key]] = values[key]
            except:
                invalid_inputs.add(key)

        elif key == '-DHCP-':
            map_valid_input_values[map_inputs[key]] = values[key]

        elif (key == "-IMAGE-" or key == "-EMBEDED_SRC-" or 
                key == "-FARMSERVER-" or key == "-FARMSERVERF1INSTALLER-" or
                key == "-DB_FILE-" or key == "-NAND_SRC_PATH-" or key == "-DB_FILE_SRC-"):
            
            if not CheckValidFilePath(value, key):
                invalid_inputs.add(key)
            else:
                map_valid_input_values[map_inputs[key]] = values[key]

        elif key == "-IMPORTDBBOOL-":
            map_valid_input_values[map_inputs[key]] = values[key]
    if len(invalid_inputs) == 0:
        isValid = True
    return isValid