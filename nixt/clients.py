# This file is placed in the Public Domain.


"client-side event handling"


import logging
import queue
import threading
import _thread


from nixt.brokers import Broker
from nixt.command import Commands
from nixt.handler import Handler
from nixt.threads import launch


class Client(Handler):

    def __init__(self):
        super().__init__()
        self.olock = threading.RLock()
        self.oqueue = queue.Queue()
        self.silent = True
        Broker.add(self)

    def announce(self, text):
        if not self.silent:
            self.raw(text)

    def display(self, event):
        with self.olock:
            for tme in event.result:
                txt = event.result.get(tme)
                self.dosay(event.channel, txt)

    def dosay(self, channel, text):
        self.say(channel, text)

    def raw(self, text):
        raise NotImplementedError("raw")

    def say(self, channel, text):
        self.raw(text)

    def wait(self):
        try:
            self.oqueue.join()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


class CLI(Client):
 
     def __init__(self):
         super().__init__()
         self.register("command", Commands.command)


class Output(Client):

    def output(self):
        while True:
            event = self.oqueue.get()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def start(self):
        launch(self.output)
        super().start()

    def stop(self):
        self.oqueue.put(None)
        super().stop()


def __dir__():
    return (
        'Client',
        'CLI',
        'Output'
    )
