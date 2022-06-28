import os.path as op
import ipaddress
import PySimpleGUI as sg
import os.path

row1Validations = []
row2Validations =[]
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
mapValidInputValues = {}
#-------------------ADDING DEFAULT VALUES IN DEV MODE--------------------------
defaultPathvalues = {
    '-IMAGE-' : 'image_5.19.0.gz',
    '-EMBEDED_SRC-' : 'package_1.7.0.0.tar.gz',
    '-NAND_SRC_PATH-' : 'scr-u-boot-1.0.0.0.bin',
    '-DB_FILE-' : 'baseline_db_3.4.0.63644_new.sql',
    "-DB_FILE_SRC-" : 'baseline_db_3.4.0.63644_new.sql',
    '-FARMSERVER-' : 'F1-Installer-5.19.0_7.0.5.jar',
    '-FARMSERVERF1INSTALLER-' : 'F1-Installer-5.19.0_7.0.5.jar'
    }
defaultValues = {
    '-TO_RTS-' : '2560',
    '-FROM_RTS-' : '2561',
    '-SN-':"RG11SNSTFS000475" ,  #default==empty
    '-HOST_IP_INPUT-': '10.4.1.1',
    '-SOM_DESIRED_IP-' : '10.4.1.55',
}
def AttatchDefaultValues(window):
    global defaultvalues
    data_path = r"C:\Users\reine\OneDrive\Desktop\f1pygui\f1Data"
    for key,value in defaultPathvalues.items():
        window[key](op.join(data_path,(value + '.txt')))
    for key, value in defaultValues.items():
        window[key](value)
#---------------------ADDING DEFAULT VALUES IN DEV MODE------------------------------------


def ThrowPopUpError():
    global row1Validations
    global row2Validations
    global mapInputs
    invalidMarkups = []

    [invalidMarkups.append(mapInputs[x]) for x in row1Validations]
    if len(row2Validations) > 0:
        [invalidMarkups.append(mapInputs[x]) for x in row2Validations]

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
    global row1Validations
    global mapValidInputValues

    file_exten_value = True
    file_exten_value = validfile(path, forced_ext='.txt')
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
        row1Validations.append(value)
    else:
        mapValidInputValues[mapInputs[value]] = path

def Validaterow2Input(value, values):
    global row2Validations
    global mapValidInputValues
    v = values[value]
    if len(v) <= 0 or v == '':
        row2Validations.append(value)
    else:
        mapValidInputValues[mapInputs[value]] = v


def Validaterow1Input(value, values):
    global row1Validations
    global mapValidInputValues
    v = values[value]
    if len(v) <= 0 or v == '':
        row1Validations.append(value)
    else:
        mapValidInputValues[mapInputs[value]] = v


def ValidatePortLength(value, values):
    global row2Validations
    global mapValidInputValues
    v = values[value]
    if len(v) != 4:
        row2Validations.append(value)
    else:
        mapValidInputValues[mapInputs[value]] = v


def validate_ip_address_row2(value, values):
    global row2Validations
    global mapValidInputValues
    address = values[value]
    try:
        ipaddress.ip_address(address)
        mapValidInputValues[mapInputs[value]] = address
    except:
        row2Validations.append(value)
        


def validate_ip_address_row1(value, values):
    global row1Validations
    global mapValidInputValues
    address = values[value]
    try:
        ipaddress.ip_address(address)
        mapValidInputValues[mapInputs[value]] = address
    except:
        row1Validations.append(value)



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

#---------------row one elements for validation-------------------------
def ValidateRow1Inputs(values) -> list:
    global row1Validations
    row1Validations.clear()
    '''Returns list of invalid inputs from window'''
    for value in values:
        if 'BROWSE' in value.upper():
            pass
        else:
            if value == "-SERIAL_PORT-":
                Validaterow1Input(value, values)
            elif value == "-HOST_IP_INPUT-":
                validate_ip_address_row1(value, values)

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
        ThrowPopUpError()
    
    return row1Validations
#---------------row two elements for validation-------------------------]
def ValidateAllInputs(values) -> tuple:
    '''returns a tuple, first value being a boolean statement, and the second a list of invalid input elements'''
    global row2Validations
    global mapValidInputValues
    row2Validations.clear()
    isValid = False #Set to true to run development without inputs
    for value in values:
        if value == "-SN-":
            Validaterow2Input(value, values)
        elif value == "-TO_RTS-" or value == '-FROM_RTS-':
            ValidatePortLength(value, values)
        elif value == "-SOM_DESIRED_IP-":
            validate_ip_address_row2(value, values)
        elif value == '-F1_UNIT-':
            v = values[value]
            if v == 'Static':
                mapValidInputValues[mapInputs[value]] = v
                DHCP = False #not returning bool value anywhere but input value of static and dhcp returned
            elif v == 'DHCP':
                mapValidInputValues[mapInputs[value]] = v
                DHCP = True
            else:
                row2Validations.append(value)
    row1Validations = ValidateRow1Inputs(values)
    errors = row1Validations + row2Validations

    if len(errors) == 0:
        isValid = True
    return isValid, errors, mapValidInputValues.keys()


