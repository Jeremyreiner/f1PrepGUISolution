import queue
import logging
import threading
from pysimpleguiLayout import *
from guiExtensionFunctions import mapValidInputValues
import time

logger = logging.getLogger('mymain')  # global logger
progress=0

class ThreadedApp():
    def __init__(self, mapValidInputValues, log_queue, queue_handler, window, interval):
        super().__init__()
        self.stop_event = threading.Event()
        self.params = mapValidInputValues
        self.queue = log_queue
        self.handler = queue_handler
        self.window = window
        self.inerval = interval
        self.run_script = ""
        self.run_log = ""

    def run(self):
        self.run_script = threading.Thread(target=mock_script, kwargs=(self.params), args=([self.stop_event]),name="scriptThread")
        self.run_script.start()

    def runLog(self):
        global progress
        self.run_log = threading.Thread(target=run_logger, args=(self.queue, self.handler, self.window, self.inerval),name="loggerThread")
        self.run_log.start()
        global progress
        progress_stage = RequestProgress(progress)
        return progress_stage

    def stop(self):
        self.stop_event.set()
        self.run_script.join()
        self.run_log.join()
        global progress
        progress = 0


class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)

# Will be replaced by the F1_test run function.
def mock_script(*args, **kwargs):
    stop_event = args
    for key in kwargs:
        txt = f'{key}: {kwargs[key]}\n'
        logger.info(txt)
        time.sleep(1)
        if stop_event[0].is_set():
            break


def startApp(app_started, window, interval) -> tuple:
    # Setup logging and start app
    logging.basicConfig(level=logging.DEBUG)
    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)
    threadedApp = ThreadedApp(mapValidInputValues, log_queue, queue_handler, window, interval)
    if not app_started:
        threadedApp.run()
        logger.debug(f'App started\n---------------------\n')
        app_started = True
        return app_started,threadedApp

def run_logger(*args):
    log_queue, queue_handler, window, interval = args 
    global progress
    try:
        record = log_queue.get(block=False)
        msg = queue_handler.format(record)
        if msg == 'App started\n---------------------\n':
            window['-LOG-'].update(msg+'\n', append=True)
            progress += interval
        else:
            if log_queue.unfinished_tasks >= 0:
                window['-LOG-'].update(msg+'\n', append=True)
                progress += interval
                window['-PROGRESSBAR-'].update(progress)
    except queue.Empty:
        pass


def RequestProgress(progress):
    return progress


