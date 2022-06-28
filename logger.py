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
        '''
        Threaded app has three responsibilities
        1: read the script and add each item to the queue
        2: Take from the queue and add each item into the gui
        3: Terminate created threads, join each thread into the main thread, and reset the progress bar position
        '''
        self.stop_event = threading.Event()
        self.params = mapValidInputValues
        self.queue = log_queue
        self.handler = queue_handler
        self.window = window
        self.inerval = interval
        self.run_script = ""
        self.run_log = ""

    def run(self):
        '''
        Run script simply reads through the mock script and adds each item into the queue,
        This thread listens for the stop event flag, if active, will break out of the loop.
        '''
        self.run_script = threading.Thread(target=mock_script, kwargs=(self.params), args=([self.stop_event]),name="scriptThread")
        self.run_script.start()

    def runLog(self):
        '''
        RunLog thread reads from the queue, if it is empty this method waits until something is added.
        When an item is added to the queue this method retrieves it, adds it to the gui, and updates the progress bar.
        This thread will be terminated upon a stop btn event, or when the progressbar has reached its max value.
        '''
        global progress
        self.run_log = threading.Thread(target=run_logger, args=(self.queue, self.handler, self.window, self.inerval),name="loggerThread")
        self.run_log.start()
        return progress

    def stop(self):
        '''
        Sets a flag event for the run method, flagging the thread will be terminated and allowing to break out of loop.
        Then procedes to join the threads back into main thread, finally updating the progress bar 
        '''
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
        txt = f'[{key}] {kwargs[key]}\n'
        logger.info(txt)
        time.sleep(1)
        if stop_event[0].is_set():
            break


def startApp(app_started, window, interval) -> tuple:
    '''
    Configures connections for logger and queue, and initializes the threading app class.
    this returns a boolean statement needed in mainthread loop if Threading App has started.
    '''
    logging.basicConfig(level=logging.DEBUG)
    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)
    threaded_app = ThreadedApp(mapValidInputValues, log_queue, queue_handler, window, interval)
    if not app_started:
        threaded_app.run()
        logger.debug(f'App started\n---------------------\n')
        app_started = True
        return app_started,threaded_app

def run_logger(*args):
    '''
    Each iteration in the mainthread reads from this method.
    Attempts to retrieve an item from the queue, update the mainwindow log key,
    and progressbar.

    '''
    log_queue, queue_handler, window, interval = args 
    global progress
    try:
        record = log_queue.get(block=False)
        msg = queue_handler.format(record)
        if msg == 'App started\n---------------------\n':
            window['-LOG-'](msg+'\n', append=True)
            progress += interval
        else:
            if log_queue.unfinished_tasks >= 0:
                window['-LOG-'](msg+'\n', append=True)
                progress += interval
                window['-PROGRESSBAR-'](progress)
    except queue.Empty:
        pass

