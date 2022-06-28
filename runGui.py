from pysimpleguiLayout import *
from logger import *

progress

def main():
    window = Make_Win1()
    window.Maximize()
    valid_inputs_bool = False
    app_started = False
    progress_bar = window['-PROGRESSBAR-']
    interval = 0
    progress = 0
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
                progress_bar.update(0)
                interval = 100 / len(valid_inputs_List)
                window['-LOG-'].update('')
                window['-CONTINUE-'].Update(visible=False)
                window['-STOP_LOG-'].Update(visible=True)
                window['-LOADING-'].Update(visible=True)
                app_started,threaded_app = startApp(app_started,window, interval)

        elif event == "-NETWORK_SETTINGS-":
            continue

        elif event == "-OPEN_LOG_FOLDER-":
            continue
        elif event == sg.WIN_CLOSED:
            break

        if valid_inputs_bool:   
            if not app_started:
                window['-CONTINUE-'].Update(visible=True)
                window['-STOP_LOG-'].Update(visible=False)
                window['-LOADING-'].Update(visible=False)
            else:
                progress = threaded_app.runLog()
                if event == "-STOP_LOG-" or progress >= 99:
                    threaded_app.stop()
                    app_started = False
    window.close()


if __name__ == '__main__':
    main()



