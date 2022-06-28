from pysimpleguiLayout import *
from logger import *


def main():
    window = Make_Win1()
    window.Maximize()
    valid_inputs_bool,app_started = False,False
    AttatchDefaultValues(window)
    # Run a while loop for continuios iterations Event Loop
    while True:
        event, values = window.read(timeout=100)
        window['-LOADING-'].update_animation(popAnim, time_between_frames=10)
    
        if event == "-SAVE-":
            errors = ValidateRow1Inputs(values)
            HighlightIncorrectInputs(values, errors, window)
        elif event == "-CONTINUE-":
            valid_inputs_bool, errors, valid_inputs_List = ValidateAllInputs(values)
            HighlightIncorrectInputs(values, errors, window)
            if valid_inputs_bool: 
                window['-PROGRESSBAR-'](0)
                interval = 100 / len(valid_inputs_List)
                window['-LOG-']('')
                window['-CONTINUE-'](visible=False)
                window['-STOP_LOG-'](visible=True)
                window['-LOADING-'](visible=True)
                app_started,threaded_app = startApp(app_started,window, interval)
        elif event == "-NETWORK_SETTINGS-":
            continue
        elif event == "-OPEN_LOG_FOLDER-":
            continue
        elif event == sg.WIN_CLOSED:
            break
        if valid_inputs_bool:   
            if not app_started:
                window['-CONTINUE-'](visible=True)
                window['-STOP_LOG-'](visible=False)
                window['-LOADING-'](visible=False)
            else:
                progress = threaded_app.runLog()
                if event == "-STOP_LOG-" or progress >= 99:
                    threaded_app.stop()
                    app_started = False
    window.close()

if __name__ == '__main__':
    main()
