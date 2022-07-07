from Tests.F1_unit_prep.F1_unit_prep import *
from Tests.F1_unit_prep.f1PrepGUI.store_handler import *
from guiValidationFunctions import *
from pysimpleguiLayout import *
from DefaultValues import *
import os
import logging
import threading
import ctypes

logger = logging.getLogger('f1_unit_prep')  # global logger
global guiSteps


class ThreadedApp(threading.Thread):
    def __init__(self, params):
        super().__init__()
        self._stop_event = threading.Event()
        self.params = params

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

    def stop(self):
        self.raise_exception()
        self.join()
        logger.error("F1_unit_prep script was stopped by the user.")

    def run(self):
        F1 = F1_Unit_Prep(gui_params=self.params, logger=logger)
        F1.run()


highlighted_inputs = set()
def HighlightIncorrectInputs(window):
    global highlighted_inputs
    if len(invalid_inputs) > 0:
        for error in invalid_inputs:
            if not error == "-SERIAL_PORT-" and not error == "-DHCP-" and not error == '-IMPORTDBBOOL-':
                window[error](background_color="gray")
                highlighted_inputs.add(error)


def FixHighlightedInputs(window):
    if len(highlighted_inputs) > 0:
        for value in highlighted_inputs:
            if value not in invalid_inputs:
                window[value](background_color="white")
    highlighted_inputs.clear()


def main():
    global progress
    window = Make_Win1()
    window.Maximize()
    progress_bar = window['progressbar']
    progress = 0
    threadedApp = 0
    isValid = False

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

        if event == '-IMPORTDBBOOL-':
            window['-DB_FILE_SRC-'].update(disabled=not values['-IMPORTDBBOOL-'])

        if event == "-SAVE-":
            isValid = ValidateAllInputs(values)
            FixHighlightedInputs(window)
            settings = SettingsRow(invalid_inputs)
            if len(settings) > 0:
                HighlightIncorrectInputs(window)
                input_var = "FIELDS" if len(invalid_inputs) > 1 else "FIELD"
                sg.PopupError(f'To save settings, correct the folowing {input_var}\n{printError(settings)}',
                                title=("SAVING ERROR"))
            else:
                data = load_data()
                for field in data:
                    if field in v_to_g:
                        gfield = v_to_g[field]
                        if gfield in values:
                            data[field] = values[gfield]
                dump_data(data)
                sg.popup_auto_close("Parameters Saved")

        elif event == '-NETWORK_SETTINGS-':
            os.system('ncpa.cpl')

        elif event == "-CONTINUE-":
            isValid = ValidateAllInputs(values)
            FixHighlightedInputs(window)
            if not isValid:
                HighlightIncorrectInputs(window)
                input = "INPUTS" if len(invalid_inputs) > 1 else "INPUT"
                sg.PopupError(
                    f'TO RUN THE PROGRAM THE FOLLOWING {input} MUST BE CORRECTED\n {printError(invalid_inputs)}',
                    title=("RUNTIME ERROR"))
            if isValid:
                window['-LOG-']('')
                window['-CONTINUE-'](visible=False)
                window['-STOP_LOG-'](visible=True)
                window['-LOADING-'](visible=True)
                threadedApp = ThreadedApp(data)
                threadedApp.start()
                logger.debug(f'App started\n---------------------\n')
                interval = int(100 / len(values.keys()))
                for field in data:
                    if field in v_to_g:
                        gfield = v_to_g[field]
                        if gfield in values:
                            data[field] = values[gfield]
                dump_data(data)

        elif event == "-OPEN_LOG_FOLDER-":
            continue

        elif event == sg.WIN_CLOSED:
            if not isinstance(threadedApp, int):
                threadedApp.stop()
            break

        if event == '-STOP_LOG-':
            progress = 0
            progress_bar.UpdateBar(0)
            window['-CONTINUE-'](visible=True)
            window['-STOP_LOG-'](visible=False)
            window['-LOADING-'](visible=False)
            if not isinstance(threadedApp, int):
                threadedApp.stop()
            continue

    window.close()


if __name__ == '__main__':
    main()