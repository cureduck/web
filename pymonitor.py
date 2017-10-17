from multiprocessing import Process
import os,sys,time

from app import run_server
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def log(s):
    print('[Monitor] %s' % s)

class MyFileSystemEventHander(FileSystemEventHandler):

    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            log('Python source file changed: %s' % event.src_path)
            self.restart()

process=None

def kill_process():
    global process
    if process:
        log('Kill process [%s]...' % process.pid)
        process.terminate()
        log('Process ended with code %s.' % process.exitcode)
        process = None

def start_process():
    global process
    process = Process(target=run_server)
    process.start()


def restart_process():
    kill_process()
    start_process()


def start_watch(path,callback):
    observer=Observer()
    observer.schedule(MyFileSystemEventHander(restart_process),path,recursive=True)
    observer.start()
    log('Watching directory %s...' % path)
    start_process()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__=='__main__':
    path=os.path.abspath('.')
    start_watch(path,None)

