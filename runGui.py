from pysimpleguiLayout import *
from DefaultValues import *
from logger import *
from guiExtensionFunctions import invalid_inputs,v_to_g, ValidateAllInputs, invalid_inputs


highlighted_inputs = set()
def HighlightIncorrectInputs(window):
    global highlighted_inputs
    if len(invalid_inputs) > 0:
        for error in invalid_inputs:
            if not error == "-SERIAL_PORT-" and not error == "-DHCP-" and not error == '-IMPORTDBBOOL-':
                window[f'{error}'](background_color = "gray")
                highlighted_inputs.add(error)


def FixHighlightedInputs(window):
    if len(highlighted_inputs) > 0:
        for value in highlighted_inputs:
            if value not in invalid_inputs:
                window[f'{value}'](background_color = "white")
        highlighted_inputs.clear()


def main():
    global progress
    window = Make_Win1()
    window.Maximize()
    valid_inputs_bool, app_started = False, False
    values = {}
    
    data = load_data() #Pull json object and fill window
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
            FixHighlightedInputs(window)
            settings = ValidateSettings(invalid_inputs)
            if len(settings) > 0:
                HighlightIncorrectInputs(window)
                input = "FIELDS" if len(invalid_inputs) > 1 else "FIELD"
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
            FixHighlightedInputs(window)
            if not valid_inputs_bool:
                HighlightIncorrectInputs(window)
                input = "INPUTS" if len(invalid_inputs) > 1 else "INPUT"
                sg.PopupError(f'TO RUN THE PROGRAM THE FOLLOWING {input} MUST BE CORRECTED\n {printError(invalid_inputs)}', title=("RUNTIME ERROR"))
            if valid_inputs_bool: 
                window['-LOG-']('')
                window['-CONTINUE-'](visible=False)
                window['-OPEN_LOG_FOLDER-'](visible=False)
                window['-STOP_LOG-'](visible=True)
                window['-LOADING-'](visible=True)
                app_started, ThreadedApp = startApp(app_started)
                for field in data:
                    if field in v_to_g:
                        gfield = v_to_g[field]
                        if gfield in values:
                            data[field] = values[gfield]
                dump_data(data)

        elif event == "-NETWORK_SETTINGS-":
            continue

        elif event == "-OPEN_LOG_FOLDER-":
            continue
        elif event == sg.WIN_CLOSED:
            if app_started:
                if not isinstance(ThreadedApp, int):
                    ThreadedApp.stop()
            break

        if valid_inputs_bool:   
            if not app_started:
                window['-CONTINUE-'](visible=True)
                window['-OPEN_LOG_FOLDER-'](visible=True)
                window['-STOP_LOG-'](visible=False)
                window['-LOADING-'](visible=False)
            else:
                # PROGRESS BAR IS DISCONEECTED WITH SG.OUTPUT
                if event == "-STOP_LOG-":
                    app_started = ThreadedApp.stop()
                    if not isinstance(ThreadedApp, int):
                        ThreadedApp.stop()


                # try:
                #     record = log_queue.get(block=False)
                #     msg = queue_handler.format(record)
                #     window['-LOG-'](msg+'\n', append=True)
                #     progress += interval
                #     if msg != 'App started\n---------------------\n':
                #         window['-PROGRESSBAR-'](progress)
                # except queue.Empty:
                #     pass
                # if event == "-STOP_LOG-" or progress >= 99:
                #     app_started = ThreadedApp.stop()
                #     if not isinstance(ThreadedApp, int):
                #         ThreadedApp.stop()
                #         progress = 0
                #     continue
    window.close()



if __name__ == '__main__':
    main()