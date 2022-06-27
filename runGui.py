from pysimpleguiLayout import *
from logger import *

def main():
    window = Make_Win1()
    window.Maximize()
    progress_bar = window['progressbar']
    progress = 0
    isValid = False
    app_started = False

    # Run a while loop for continuios iterations Event Loop
    while True:
        event, values = window.read(timeout=100)

        window['-LOADING-'].update_animation(popAnim, time_between_frames=10)

        if event == "-SAVE-":
            errors = ValidateRow1Inputs(values)
            HighlightIncorrectInputs(errors, window)

        elif event == "-CONTINUE-":
            isValid, errors, isValidList = ValidateAllInputs(values)
            HighlightIncorrectInputs(values, errors, window)
            if isValid: 
                interval = int(100 / len(isValidList))
                window['-CONTINUE-'].Update(visible=False)
                window['-STOP_LOG-'].Update(visible=True)
                window['-LOADING-'].Update(visible=True)
                # threadedApp, app_started, threading = startApp(app_started,window)
                app_started,threaded_app = startApp(app_started,window)

        elif event == "-NETWORK_SETTINGS-":
            continue

        elif event == "-OPEN_LOG_FOLDER-":
            continue
        elif event == sg.WIN_CLOSED:
            break
        if isValid:    
            if not app_started:
                window['-CONTINUE-'].Update(visible=True)
                window['-STOP_LOG-'].Update(visible=False)
                window['-LOADING-'].Update(visible=False)
            else:
                threaded_app.runLog()
                # update bar with runlogs intervals and fix timing of all three threads for simultaneus events
                progress += interval
                progress_bar.update(progress)
                if event == "-STOP_LOG-":
                    threaded_app.stop()
                    app_started = False
                    progress = 0
                    progress_bar.update(progress)
                    window['-LOG-'].update('')
    window.close()


if __name__ == '__main__':
    main()



