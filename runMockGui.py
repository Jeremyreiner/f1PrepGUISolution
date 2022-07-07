import os
from pysimpleguiLayout import *
from DefaultValues import *
from logger import *
from guiValidationFunctions import invalid_inputs,v_to_g, ValidateAllInputs, invalid_inputs, SettingsRow
from plyer import notification

highlighted_inputs = set()
def HighlightIncorrectInputs(window):
    global highlighted_inputs
    for error in invalid_inputs:
        if not error == "-SERIAL_PORT-" and not error == "-DHCP-" and not error == '-IMPORTDBBOOL-':
            window[f'{error}'](background_color = "gray")
            highlighted_inputs.add(error)


def FixHighlightedInputs(window):
    global highlighted_inputs
    for value in highlighted_inputs:
        if value not in invalid_inputs:
            window[f'{value}'](background_color = "white")
    highlighted_inputs.clear()
def Notify(m ="", t=""):
    notification.notify(
        title= t,
        message= m,
        app_name="Dialogue Title",
        app_icon = None,
        timeout= 10,
        ticker="Maldita perra",
        toast=False)

def main():
    window = Make_Win1()
    window.bind('<Configure>', "-CONFIGURE-")
    window.Maximize()
    valid_inputs_bool, app_started = False, False
    values = {}

    
    data = load_data() #Pull json object and fill window
    data = load_data_by_id(data[0])
    for field in data:
        if field in v_to_g:
            gfield = v_to_g[field]
            if gfield in window.AllKeysDict:
                window[gfield](data[field])

    while True:
        event, values = window.read(timeout=100)
        window['-LOADING-'].update_animation(popAnim, time_between_frames=10)

        if event == "-SAVE-":
            valid_inputs_bool = ValidateAllInputs(values)
            if len(highlighted_inputs) > 0:
                FixHighlightedInputs(window)
            settings = SettingsRow(invalid_inputs)
            if len(settings) > 0:
                HighlightIncorrectInputs(window)
                input = "fields" if len(settings) > 1 else "field"
                sg.PopupError(f'To save settings, correct the folowing {input}\n{printError(settings)}', title=("SAVING ERROR"))
            else:
                data = load_data()
                for field in data:
                    if field in v_to_g:
                        gfield = v_to_g[field]
                        if gfield in values:
                            data[field] = values[gfield]
                dump_data(data)
                sg.Popup('SUCCESFULL SAVE')
        elif event == '-NETWORK_SETTINGS-':
            os.system('ncpa.cpl')

        elif event == "-CONTINUE-":
            valid_inputs_bool = ValidateAllInputs(values)
            if len(highlighted_inputs) > 0:
                FixHighlightedInputs(window)
            if not valid_inputs_bool:
                HighlightIncorrectInputs(window)
                input = "INPUTS" if len(invalid_inputs) > 1 else "INPUT"
                sg.PopupError(f'TO RUN THE PROGRAM THE FOLLOWING {input} MUST BE CORRECTED\n {printError(invalid_inputs)}', title=("RUNTIME ERROR"))
            else: 
                window['-LOG-']('')
                window['-CONTINUE-'](visible=False)
                window['-STOP_LOG-'](visible=True)
                window['-LOADING-'](visible=True)
                for field in data:
                    if field in v_to_g:
                        gfield = v_to_g[field]
                        if gfield in values:
                            data[field] = values[gfield]
                dump_data(data)
                app_started, ThreadedApp = startApp(app_started)

        elif event == "-OPEN_LOG_FOLDER-":
            os.system('f1pygui')
        elif event == sg.WIN_CLOSED:
            if app_started:
                if not isinstance(ThreadedApp, int):
                    ThreadedApp.stop()
            break

        if valid_inputs_bool:   
            if not app_started:
                window['-CONTINUE-'](visible=True)
                window['-STOP_LOG-'](visible=False)
                window['-LOADING-'](visible=False)
            else:
                progress =RetrieveProgress()
                window["-PROGRESSBAR-"](progress)
                if event == "-STOP_LOG-":
                    if not isinstance(ThreadedApp, int):
                        app_started = ThreadedApp.stop()
                        title= "Script Event Been Stopped By User"
                        message= "Open F1 App To See The Occurence"
                        Notify(message, title)
                elif progress >= 100:
                    if not isinstance(ThreadedApp, int):
                        app_started = ThreadedApp.stop()
                        title= "F1 Script Completed"
                        message= "Open F1 App For Next Steps"
                        Notify(message, title)

    window.close()



if __name__ == '__main__':
    main()