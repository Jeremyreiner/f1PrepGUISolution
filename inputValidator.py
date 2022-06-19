from pathlib import Path
import PySimpleGUI as sg
import os.path

def ValidateInput(values) -> tuple:
    '''Returns tuple (success, extraction_type)'''
    global indx
    i_path = values[0] # input file/folder
    ext_type = ''

    if len(i_path) == 0:
        sg.PopupError('No INPUT file or folder selected!')
        return False, ext_type
    elif not os.path.exists(i_path):
        sg.PopupError('INPUT file/folder does not exist!')
        return False, ext_type
    elif os.path.isdir(i_path):
        ext_type = 'fs'
    else: # must be an existing file then
        if i_path.lower().endswith('.tar') and not i_path.lower().endswith('.zip'):
            sg.PopupError('Input file is not a supported archive! ', i_path)
            return False, ext_type
        else:
            ext_type = Path(i_path).suffix[1:].lower() 

    return True, ext_type


def ValidateSPComboBox(values):
    sp = values["-SERIAL_PORT-"]
    if (len(sp) != 0):
        is_valid = True
        values["-HOST_IP-"] = sp
    else:
        is_valid = False
    return is_valid, 