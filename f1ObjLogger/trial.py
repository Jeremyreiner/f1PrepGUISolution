import json
import random
import threading
import time
from faker import Faker
from threading import Thread


fake = Faker()
rwlock = threading.RLock()


def add_person(data, id, path):
    person = {
        "id": id,
        "name": fake.name(),
        "age": random.randint(18, 100),
        "gender": random.choice(["female", "Male"])
        }

    data.append(person)

    dump_json(path, data)
    

def dump_json(path, data):
    rwlock.acquire()
    try:
        with open(path, "w") as f:
            json.dump(data, f,indent=2)
    finally:
        #Release the write lock
        rwlock.release()


def read_json(path):
    rwlock.acquire()
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    finally:
        #Release the write lock
        rwlock.release()


class RunThread():
    def __init__(self,data,iter, path):
        self.data = data
        self.path = path
        self.iter = iter

    def Run(self):
        self.running = True
        self.stop = False
        while self.running:
            add_person(self.data, self.iter,self.path)

            if self.stop:
                self.running = False

            self.iter += 1
            time.sleep(1)

    def Stop(self):
        self.stop = True

if __name__ == '__main__':
    path = r'C:\Users\Jeremy\OneDrive\WorkPC\f1pygui\f1ObjLogger\demo.json'
    
    data = read_json(path)
    
    jsonThread = Thread(target=RunThread(data, len(data), path).Run)

    jsonThread.start()

