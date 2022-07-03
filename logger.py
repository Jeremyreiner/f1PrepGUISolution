import time
import queue
import logging
import threading
import ctypes
from guiExtensionFunctions import map_valid_input_values #used for logging in mockscript

logger = logging.getLogger('f1_unit_prep')  # global logger

class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)

class ThreadedApp(threading.Thread):
    def __init__(self, map_valid_input_values):
        super().__init__()
        self._stop_event = threading.Event()
        self.params = map_valid_input_values

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
        logger.info("F1_unit_prep script was stopped by the user.")
        self._stop_event.set()
        self.run_script.join()
        return False

    def run(self):
        self.run_script = threading.Thread(target=mock_script, args=([self._stop_event], self.params),name="scriptThread")
        self.run_script.start()


# Will be replaced by the F1_test run function.
def mock_script(*args):
    stop_event, inputs = args
    for key in inputs:
        txt = f'[{key}] {inputs[key]}\n'
        logger.info(txt)
        time.sleep(1)
        if stop_event[0].is_set():
            break


def startApp(app_started) -> tuple:
    '''
    Configures connections for logger and queue, and initializes the threading app class.
    This returns a boolean statement needed in mainthread loop if Threading App has started.
    '''
    logging.basicConfig(level=logging.DEBUG)
    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)
    threaded_app = ThreadedApp(map_valid_input_values)
    if not app_started:
        threaded_app.run()
        logger.info(f'App started\n---------------------\n')
        app_started = True
        return app_started, threaded_app
    else:
        return app_started, threaded_app

