from concurrent.futures import thread
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
        self._stop_event = threading.Event()
        self.params = mapValidInputValues
        self.queue = log_queue
        self.handler = queue_handler
        self.window = window
        self.inerval = interval

    def run(self):
        x = threading.Thread(target=mock_script, kwargs=(self.params))
        x.start()

    def runLog(self):
        x = threading.Thread(target=run_logger, args=(self.queue, self.handler, self.window, self.inerval ))
        x.start()

        #run_logger(self.queue, self.handler, self.window)

    def stop(self):
        global progress
        progress = 0
        self._stop_event.set()

class QueueHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)

# Will be replaced by the F1_test run function.
def mock_script(**kwargs):
    for key in kwargs:
        txt = f'{key}: {kwargs[key]}\n'
        logger.info(txt)
        time.sleep(1)

def startApp(app_started, window, interval) -> tuple:
    # Setup logging and start app
    logging.basicConfig(level=logging.DEBUG)
    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)
    logger.addHandler(queue_handler)
    #threaded_app = ThreadedApp(mapValidInputValues)
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
        else:
            if log_queue.unfinished_tasks >= 1:
                time.sleep(1)
                window['-LOG-'].update(msg+'\n', append=True)
                progress += interval
                window['-PROGRESSBAR-'].update(progress)
    except queue.Empty:
        pass



#fix logging for actual que and not reiterating over list 

'''
--Levels of logging --
DEBUG -  Detailed info typically of iunterest only when diagnoising problems

INFO: Confirmation that things are working as expected

ERROR: Due to ta more serious problem, the software has not been able to perform some function

CRITICAL: A serious error, indicating that the program itself may be unable to continue running
'''
'''
THREAD = a flow of execution, like a separate order of instructions. However each thread takes a turn running to achieve concurrency. 
        GIL = global interpreter lock, allows only one thread to hold the control of python interpreter at any one time
            
CPU BOUND = program task spends most of its time waiting for internal events (CPU intensive) use multiprocessing

IO BOUND = program / task spends most of its time waiting for external events (user inputs, web scraping) in multithreading
'''