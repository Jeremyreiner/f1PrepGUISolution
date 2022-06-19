from ast import Continue
import PySimpleGUI as sg
import os.path
from inputValidator import * 


selection = ('1', '2', '3', '4', '5', '6')

width = max(map(len, selection))+1
inputWidth = 25
buttonWidth = 5
inputPadding = ((3, 5))
clmnSize=(300,200)


col1 = [
        [sg.Text('Serial Port')],[sg.Combo(selection, size=((inputWidth + buttonWidth + 2), 5), enable_events=True, key='-SERIAL_PORT-', pad=inputPadding)],
        [sg.Text('Host_Ip')],[sg.Input('', size=(inputWidth,5), key='-HOST_IP_INPUT-')], 
        [sg.Button('Network Settings', pad=(2, 35), key='-NETWORK_SETTINGS-')]  
    ]
col2 = [
        [sg.Text('Image Path')],[sg.Input(size=(inputWidth,1)), sg.FileBrowse(size=(buttonWidth, 1), key='-IMAGE-', pad=inputPadding)],
        [sg.Text('Embedded_src_Path')],[sg.Input(size=(inputWidth,1)), sg.FileBrowse(size=(buttonWidth, 1),  key='-EMBEDED_SRC-',)], 
    ]
col3 = [
        [sg.Text('farmserverfillsrc')], [sg.Input(size=(inputWidth,1)), sg.FileBrowse(size=(buttonWidth, 1), key='-FARMSERVER-', pad=inputPadding)],
        [sg.Text('farmserverf1installersrc')], [sg.Input(size=(inputWidth,1)), sg.FileBrowse(size=(buttonWidth, 1), key='-FARMSERVERF1INSTALLER-', pad=inputPadding)],
        [sg.Text('pathtodbfile')], [sg.Input(size=(inputWidth,1)), sg.FileBrowse(size=(buttonWidth, 1), key='-DB_FILE-',)]  
    ]
col4 = [
        [sg.Text('import database')],[sg.Input(size=(inputWidth,1)), sg.Checkbox('', size=(buttonWidth, 1), key='-IMPORTDB-',pad=inputPadding)],
        [sg.Text('nand_src_path')],[sg.Input(size=(inputWidth,1)), sg.FileBrowse(size=(buttonWidth, 1), key='-NAND_SRC_PATH-', pad=inputPadding)], 
        [sg.Text('dbfilesrc')],[sg.Input(size=(inputWidth,1)), sg.FileBrowse(size=(buttonWidth, 1), key='-DB_FILE_SRC-',)]  
    ]
col5 = [
        [sg.Button('Save Settings', pad=((5, 170)), key='-SAVE-',)]  
    ]

row2Col1 = [
        [sg.Text('Serial Number- AZ304i234')],[sg.Input(size=(inputWidth,1), pad=inputPadding, key='-SN-')],
        [sg.Text("TO_RTS_PORT (1000-65535)")],[sg.Input(size=(inputWidth,1), pad=inputPadding,  key='-TO_RTS-',)], 
        [sg.Text("FROM_RTS_PORT (1000-65535)")],[sg.Input(size=(inputWidth,1),  key='-FROM_RTS-',)],
    ]
row2Col2 = [
        [sg.Text("som_desired_ip")],[sg.Input(size=(inputWidth,1), pad=inputPadding, key='-SOM_DESIRED_IP-')],
        [sg.Text('f1_unit_prep_final_ip_config')],[sg.Input(size=(inputWidth,1)), sg.Button('DHCP/\nstatic', size=(buttonWidth,2),key='-F1_UNIT_PREP_FINAL_IP-', pad=inputPadding)], 
    ]
row2Col3 = [
        [sg.Text('')],
    ]
row2Col4 = [
        [sg.Text('')],
    ]
row2Col5 = [
        [sg.Button('Continue', pad=(50), key='-CONTINUE-')],
        [sg.Button('Open Log Folder', pad=(5,30), key='-OPEN_LOG_FOLDER-')]
    ]

#-------ROW DESIGN INSIDE OF WINDOW----------------
row1 =[[
        sg.Frame('Settings',
        [[
            sg.Col(col1, p=0, size=(clmnSize)), sg.Col(col2, p=0, size=(clmnSize)),
            sg.Col(col3, p=0, size=(clmnSize)),sg.Col(col4, p=0, size=(clmnSize)),
            sg.Col(col5, p=0, size=(clmnSize))
        ]])
    ]]

row2 = [[
        sg.Col(row2Col1, p=0, size=(clmnSize)), sg.Col(row2Col2, p=0, size=(clmnSize)),
        sg.Col(row2Col3, p=0, size=(clmnSize)),sg.Col(row2Col4, p=0, size=(clmnSize)),
        sg.Col(row2Col5, p=0, size=(clmnSize)),
    ]]

row3 = [
    [sg.Text('Status Notes')],
    [sg.Multiline(size=(175, 10), key='texbox')]
    ]
#-------ROW DESIGN INSIDE OF WINDOW----------------

ProgressBarAtFoot = [
    [sg.ProgressBar(1000, orientation='h', size=(113, 20), key='progressbar')],
    ]

layout = [
    [
        [row1, row2, row3, ProgressBarAtFoot]
    ]
]

window = sg.Window("Dialog Title", layout)
progress_bar = window['progressbar']
i = 0

is_valid = False
inValidList = []
# Run a while loop for continuios iterations Event Loop
while True:
    event, values = window.read()
    progress_bar.UpdateBar(i + 50)

    # if event == "-IMAGE-":
    if event == "-NETWORK_SETTINGS-":
        continue
    elif event == "-SAVE-":
        continue
    elif event == "OPEN_LOG_FOLDER":
        continue
    elif event == "-F1_UNIT_PREP_FINAL_IP-":
        continue
    elif event == "-CONTINUE-":
        result = ValidateInput(values)
window.close()



#-form validation
#1- press on run check that all inputs are valid inputs