# This file is placed in the Public Domain.


"watching files"


import os
import time


from .looping import Loop


e = os.path.exists


class Watcher(Loop):

    sleep = 1.0
    cbs = {}
    times = {}

    def add(self, path, callback):
        "add callback"
        if not e(path):
            return
        self.cbs[path] = callback

    def init(self, times={}):
        "read timestamps."
        for path in self.cbs:
            if not e(path):
                continue
            self.times[path] = times.get(path, os.stat(path).st_mtime)

    def loop(self):
        "loop select."
        while not self.stopped.isSet():
            for path in self.cbs:
                if not e(path):
                    continue
                mtime = os.stat(path).st_mtime
                if mtime > self.times[path]:
                    self.cbs[path]()
                self.times[path] = mtime
            time.sleep(self.sleep)


def __dir__():
    return (
        'Watcher',
    )
