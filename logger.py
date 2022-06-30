import queue
import logging
import threading
import time
from pysimpleguiLayout import *
from guiExtensionFunctions import mapValidInputValues

logger = logging.getLogger('mymain')

class ThreadedApp():
    def __init__(self, mapValidInputValues):
        super().__init__()
        '''
        Threaded app has two responsibilities
        1: read the script and add each item to the queue
        2: Terminate created threads, join each thread into the main thread, and reset the progress bar position
        '''
        self.stop_event = threading.Event()
        self.params = mapValidInputValues
        self.run_script = ""

    def run(self):
        '''
        Run script simply reads through the mock script and adds each item into the queue,
        This thread listens for the stop event flag, if active, will break out of the loop.
        '''
        self.run_script = threading.Thread(target=mock_script, args=([self.stop_event], self.params),name="scriptThread")
        self.run_script.start()


    def stop(self):
        '''
        Sets a flag event for the run method, flagging the thread will allow access to break out of loop.
        Then procedes to join the thread back into main thread.
        '''
        self.stop_event.set()
        self.run_script.join()
        return False


class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)

# Will be replaced by the F1_test run function.
def mock_script(*args):
    stop_event, inputs = args
    for key in inputs:
        txt = f'[{key}] {inputs[key]}\n'
        logger.info(txt)
        time.sleep(1)
        if stop_event[0].is_set():
            break


def InitializeThreadedApp():
    logging.basicConfig(level=logging.DEBUG)
    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)
    threaded_app = ThreadedApp(mapValidInputValues)
    return threaded_app, log_queue, queue_handler


def startApp(app_started) -> tuple:
    '''
    Configures connections for logger and queue, and initializes the threading app class.
    This returns a boolean statement needed in mainthread loop if Threading App has started.
    '''
    threaded_app, log_queue, queue_handler =InitializeThreadedApp()
    if not app_started:
        threaded_app.run()
        logger.debug(f'App started\n---------------------\n')
        app_started = True
        return app_started, log_queue, queue_handler,threaded_app
    else:
        return app_started, log_queue, queue_handler,threaded_app

