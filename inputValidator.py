from pathlib import Path
import ipaddress
import PySimpleGUI as sg
import os.path

inValidList = []
isValid = True

def ValidateRow1Inputs(values):
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

    ThrowPopUpError(inValidList)


def ThrowPopUpError(inValidList):
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
    if type(path) == bool:
        pass
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
        #is image path
        if (path.lower().endswith('.jpeg') or path.lower().endswith('.png')
            or path.lower().endswith('.png') or path.lower().endswith('.webp') 
            or path.lower().endswith('.svg') or path.lower().endswith('.gz')):
            if value != '-IMAGE-':
                inValidList.append(value)
                isValid = False
        #is embedded_src_path, nand_src_path
        elif (path.lower().endswith('.gz') or path.lower().endswith('.bin')):
            if value != '-EMBEDED_SRC-' and value != '-NAND_SRC_PATH-' :
                inValidList.append(value)
                isValid = False
        #is database path
        elif (path.lower().endswith('.sql') or path.lower().endswith('.json') or path.lower().endswith('.exe')):
            if value != '-DB_FILE-' and value != '-DB_FILE_SRC-' and value != '-IMPORTDB-' :
                inValidList.append(value)
                isValid = False
        #is farmerserver path
        elif (path.lower().endswith('.jar') or path.lower().endswith('.sh')):
            if value != '-FARMSERVERF1INSTALLER-' and value != '-FARMSERVER-':
                inValidList.append(value)
                isValid = False
        else:
            ext_type = Path(path).suffix[1:].lower() 
            print(f"Found in else: {value}, {ext_type}")



def ValidateInput(value, values):
    v = values[value]
    if len(v) <= 0 or v == '':
        inValidList.append(value)
        isValid = False

def ValidatePortLength(value, values):
    v = values[value]
    if len(v) != 4:
        inValidList.append(value)
        isValid = False

def validate_ip_address(value, values):
    add = values[value]
    try:
        ip = ipaddress.ip_address(add)
        print("IP address {} is valid. The object returned is {}".format(add, ip))
    except:
        inValidList.append(value)
        isValid = False

#---------------row two elements for validation-------------------------]
def ValidateRow2Inputs(values):
    
    
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
                dhcp = True
            else:
                inValidList.append(value)
                isValid = False
        else:
            pass
    ValidateRow1Inputs(values)



# serial_number= "RG11SNSTFS000475"   #default==empty
# TO_RTS_PORT = '2560'
# FROM_RTS_PORT = '2561'
# som_desired_ip = '10.4.1.55'
# f1_unit_prep_final_ip_config = False #True DHCP, False static