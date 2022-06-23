import queue
import logging
import threading
from pysimpleguiLayout import *
from guiExtensionFunctions import mapInputValues

logger = logging.getLogger('mymain')  # global logger
# Will be replaced by the F1_test run function.
def mock_script(d: dict):
    for key in d:
        txt = f'{key},{d[key]}\n'
        logger.info(txt)
    

class ThreadedApp(threading.Thread):
    def __init__(self, params):
        super().__init__()
        self._stop_event = threading.Event()
        self.params = params

    def run(self):
        mock_script(self.params)

    def stop(self):
        self._stop_event.set()


class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)

def run_logger(event) -> list:
    logs = []
    appStarted = False
    # Setup logging and start app
    logging.basicConfig(level=logging.DEBUG)
    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)
    while True:
        if len(mapInputValues) > 0: # if statement used only for dev purposes
            params = mapInputValues
        threadedApp = ThreadedApp(params)
        print(len(params.keys()))
        if appStarted is False:
            threadedApp.start()
            logger.debug(f'App started\n---------------------\n')
            appStarted = True
        elif event in  (None, 'Exit'):
            break

        # Poll queue
        try:
            record = log_queue.get(block=False)
        except queue.Empty:
            pass
        else:
            msg = queue_handler.format(record)
            logs.append(msg)
            if len(logs) == len(params.keys()):
                return logs