from pysimpleguiLayout import *
from logger import *
import time

def main():
    global progress
    window = Make_Win1()
    window.Maximize()
    progress_bar = window['progressbar']
    progress = 0
    isValid = False
    msgs= []
    # Run a while loop for continuios iterations Event Loop
    while True:
        event, values = window.read(timeout=100)

        window['-LOADING-'].update_animation(popAnim, time_between_frames=10)

        if event == "-SAVE-":
            errors = ValidateRow1Inputs(values)
            HighlightIncorrectInputs(values, errors, window)

        elif event == "-CONTINUE-":
            isValid, isValidList = ValidateAllInputs(values)
            HighlightIncorrectInputs(values, isValidList, window)
            if isValid: 
                window['-CONTINUE-'].Update(visible=False)
                window['-LOADING-'].Update(visible=True)
                #check with ori about using play button / loading button swap locations
                #if loading button is over play button return line 58, 31
                #window['-OPEN_LOG_FOLDER-'].Update(visible=False)
                msgs = run_logger(event)
                interval = int(100/len(values.keys()))
                isValid = False

        elif event == "-NETWORK_SETTINGS-":
            continue

        elif event == "-OPEN_LOG_FOLDER-":

            continue
        elif event == sg.WIN_CLOSED:
            break
        if len(msgs) > 0:
            msgs = [x.replace(",", ": ") for x in msgs]
            progress += interval
            progress_bar.UpdateBar(progress)
            window['-LOG-'].update(f' {msgs[0]}\n', append=True)
            msgs.remove(msgs[0])
            if event == '-STOP_LOG-':
                #write a log on stop returns an empty log and returns the continue button to screen
                msgs.clear()
                progress = 0
                progress_bar.UpdateBar(0)
                window['-LOADING-'].Update(visible=False)
                window['-CONTINUE-'].Update(visible=True)
                #check with ori about using play button / loading button swap locations
                #if loading button is over play button return line 58, 31
                #window['-OPEN_LOG_FOLDER-'].Update(visible=True) 
                window['-LOG-'].update('')
                continue
            time.sleep(.20)
    window.close()


if __name__ == '__main__':
    main()