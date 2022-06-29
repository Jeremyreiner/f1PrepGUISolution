from pysimpleguiLayout import *
from logger import *
from DefaultValues import AttatchDefaultValues, UpdateDefaultValues
progress =0

def run_logger(*args):
    '''
    Each iteration in the mainthread reads from this method.
    Attempts to retrieve an item from the queue, update the mainwindow log key,
    and progressbar.
    '''
    log_queue, queue_handler,window, interval = args 
    global progress

    try:
        record = log_queue.get(block=False)
        msg = queue_handler.format(record)
        window['-LOG-'](msg+'\n', append=True)
        progress += interval
        if msg != 'App started\n---------------------\n':
            window['-PROGRESSBAR-'](progress)
    except queue.Empty:
        pass
    return progress


def main():
    window = Make_Win1()
    window.Maximize()
    valid_inputs_bool,app_started = False,False
    AttatchDefaultValues(window)
    global progress

    while True:
        event, values = window.read(timeout=100)
        window['-LOADING-'].update_animation(popAnim, time_between_frames=10)
    
        if event == "-SAVE-":
            valid_inputs_bool, errors, valid_inputs_List = ValidateAllInputs(values,window)
            HighlightIncorrectInputs(values, errors, window)
            UpdateDefaultValues()
        elif event == "-CONTINUE-":
            valid_inputs_bool, errors, valid_inputs_List = ValidateAllInputs(values,window)
            HighlightIncorrectInputs(values, errors, window)
            if valid_inputs_bool: 
                window['-PROGRESSBAR-'](0)
                interval = 100 / len(valid_inputs_List)
                window['-LOG-']('')
                window['-CONTINUE-'](visible=False)
                window['-STOP_LOG-'](visible=True)
                window['-LOADING-'](visible=True)
                UpdateDefaultValues()
                app_started, log_queue, queue_handler,threaded_app = startApp(app_started)
        elif event == "-NETWORK_SETTINGS-":
            continue
        elif event == "-OPEN_LOG_FOLDER-":
            continue
        elif event == sg.WIN_CLOSED:
            if app_started:
                threaded_app.stop()
            break
        if valid_inputs_bool:   
            if not app_started:
                window['-CONTINUE-'](visible=True)
                window['-STOP_LOG-'](visible=False)
                window['-LOADING-'](visible=False)
            else:
                progress = run_logger(log_queue, queue_handler,window, interval)
                if event == "-STOP_LOG-" or progress >= 99:
                    app_started = threaded_app.stop()
                    progress = 0
    window.close()

if __name__ == '__main__':
    main()
