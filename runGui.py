import queue
import logging
import threading
import ctypes
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
                window[f'{error}'](background_color = "red")
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
    progress,interval = 0, 0
    valid_inputs_bool, app_started = False, False

    data = load_data()
    for field in data:
        if field in v_to_g:
            gfield = v_to_g[field]
            if gfield in window.AllKeysDict:
                window[gfield](data[field])


    # Run a while loop for continuios iterations Event Loop
    while True:
        event, values = window.read(timeout=100)
        window['-LOADING-'].update_animation(popAnim, time_between_frames=10)

        if event == "-SAVE-":
            valid_inputs_bool, interval = ValidateAllInputs(values)
            FixHighlightedInputs(window)
            settings = ValidateSettings(invalid_inputs)
            if len(settings) > 0:
                HighlightIncorrectInputs(window)
                input = "INPUTS" if len(invalid_inputs) > 1 else "INPUT"
                sg.PopupError(f'TO SAVE SETTINGS THE FOLLOWING {input} MUST BE CORRECTED\n {printError(settings)}')
            elif len(invalid_inputs) > 0:
                HighlightIncorrectInputs(window)
            else:
                data = load_data()
                for field in data:
                    if field in v_to_g:
                        gfield = v_to_g[field]
                        if gfield in values:
                            data[field] = values[gfield]
                dump_data(data)
        elif event == '-NETWORK_SETTINGS-':
            os.system('ncpa.cpl')

        elif event == "-CONTINUE-":
            valid_inputs_bool, interval = ValidateAllInputs(values)
            FixHighlightedInputs(window)
            if not valid_inputs_bool:
                HighlightIncorrectInputs(window)
                input = "INPUTS" if len(invalid_inputs) > 1 else "INPUT"
                sg.PopupError(f'TO RUN THE PROGRAM THE FOLLOWING {input} MUST BE CORRECTED\n {printError(invalid_inputs)}')
            if valid_inputs_bool: 
                window['-LOG-']('')
                window['-CONTINUE-'](visible=False)
                window['-OPEN_LOG_FOLDER-'](visible=False)
                window['-STOP_LOG-'](visible=True)
                window['-LOADING-'](visible=True)
                for field in data:
                    if field in v_to_g:
                        gfield = v_to_g[field]
                        if gfield in window.AllKeysDict:
                            data[field] = values[gfield]
                # threadedApp = ThreadedApp(data)
                # threadedApp.start()
                # app_started = True
                # logger.debug(f'App started\n---------------------\n')
                app_started, log_queue, queue_handler,threaded_app = startApp(app_started)

        elif event == "-NETWORK_SETTINGS-":
            continue

        elif event == "-OPEN_LOG_FOLDER-":
            continue
        elif event == sg.WIN_CLOSED:
            if app_started:
                threaded_app.stop()
            break
            # if not isinstance(threadedApp, int):
            #     threadedApp.stop()
            # break

        if valid_inputs_bool:   
            if not app_started:
                window['-CONTINUE-'](visible=True)
                window['-OPEN_LOG_FOLDER-'](visible=True)
                window['-STOP_LOG-'](visible=False)
                window['-LOADING-'](visible=False)
            else:
                try:
                    record = log_queue.get(block=False)
                    msg = queue_handler.format(record)
                    window['-LOG-'](msg+'\n', append=True)
                    progress += interval
                    if msg != 'App started\n---------------------\n':
                        window['-PROGRESSBAR-'](progress)
                except queue.Empty:
                    pass
                if event == "-STOP_LOG-" or progress >= 99:
                    app_started = threaded_app.stop()
        #             if not isinstance(threadedApp, int):
        #                 threadedApp.stop()
        #             continue
                    progress = 0

    window.close()



if __name__ == '__main__':
    main()



# logger = logging.getLogger('f1_unit_prep')  # global logger

# class QueueHandler(logging.Handler):
#     def __init__(self, log_queue):
#         super().__init__()
#         self.log_queue = log_queue

#     def emit(self, record):
#         self.log_queue.put(record)


# class LogHandler(logging.Handler):
#     def __init__(self):
#         super().__init__()

#     def emit(self, record):
#         log(str(record))

# logging.basicConfig(level=logging.INFO)
# log_queue = queue.Queue()
# queue_handler = QueueHandler(log_queue)
# log_handler = LogHandler()
# logger.addHandler(queue_handler)
# logger.addHandler(log_handler)


# class ThreadedApp(threading.Thread):
#     def __init__(self, params):
#         super().__init__()
#         self._stop_event = threading.Event()
#         self.params = params

#     def get_id(self):

#         # returns id of the respective thread
#         if hasattr(self, '_thread_id'):
#             return self._thread_id
#         for id, thread in threading._active.items():
#             if thread is self:
#                 return id

#     def raise_exception(self):
#         thread_id = self.get_id()
#         res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
#               ctypes.py_object(SystemExit))
#         if res > 1:
#             ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
#             print('Exception raise failure')

#     def stop(self):
#         self.raise_exception()
#         self.join()
#         logger.error("F1_unit_prep script was stopped by the user.")

#     def run(self):
#         F1.run()
