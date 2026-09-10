# This file is placed in the Public Domain.


"an object for a string"


import logging
import queue
import threading
import time
import _thread


from .brokers import Broker
from .engines import Engine
from .looping import Loop
from .threads import Thread


class Display:

    "unit of display"

    block = threading.Event()

    def __init__(self):
        self.olock = threading.RLock()
        self.silent = False
        
    def announce(self, text):
        "announce text to all channels"
        if not self.silent:
            self.raw(text)

    def display(self, event):
        "display event results"
        with self.olock:
            for txt in event.result:
                if self.block.is_set():
                    return
                self.dosay(event.channel, txt)
                del txt
        del event

    def dosay(self, channel, text):
        "say called by display"
        self.say(channel, text)

    def raw(self, text):
        "raw output"
        raise NotImplementedError

    def say(self, channel, text):
        "say text in channel"
        self.raw(text)


class Output:

    "dedicated output loop"

    def __init__(self):
        self.oqueue = queue.Queue()
        self.ostopped = threading.Event()

    def display(self, event):
        "do actual display."

    def output(self):
        "output loop."
        while not self.ostopped.is_set():
            try:
                event = self.oqueue.get()
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()
            if event is None:
                self.oqueue.task_done()
                break
            self.display(event)
            self.oqueue.task_done()

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def start(self, daemon=True):
        "start output loop."
        self.ostopped.clear()
        Thread.launch(self.output, daemon=daemon)

    def stop(self):
        "stop output loop."
        self.ostopped.set()
        self.oqueue.put(None)

    def wait(self):
        "wait for output to finish."
        try:
            self.oqueue.join()
        except Exception as ex:
            logging.exception(ex)
            _thread.interrupt_main()


class Screen(Engine, Display):

    "display wit coupled handler"

    def __init__(self):
        Engine.__init__(self)
        Display.__init__(self)
        Broker.add(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError


class Buffer(Engine, Output):

    "buffered output"

    def __init__(self):
        Engine.__init__(self)
        Output.__init__(self)
        Broker.add(self)

    def raw(self, text):
        "raw output."
        raise NotImplementedError

    def start(self, daemon=True):
        "start output loop."
        Engine.start(self)
        Output.start(self, daemon=daemon)

    def stop(self):
        "stop output loop."
        Engine.stop(self)
        Output.stop(self)


class Clients:

    "collection of clients"

    @staticmethod
    def announce(txt):
        "announce text on all clients."
        for obj in Broker.objs("announce"):
            obj.announce(txt)

    @staticmethod
    def display(evt):
        "display results."
        bot = Broker.get(evt.orig)
        if bot:
            bot.display(evt)

    @staticmethod
    def shutdown():
        "call stop on clients."
        for client in Broker.objs("wait"):
            logging.debug("wait %s", client)
            try:
                client.wait()
            except (KeyboardInterrupt, EOFError):
                pass
        time.sleep(0.01)
        for client in Broker.objs("stop"):
            logging.debug("stop %s", client)
            try:
                client.stop()
            except (KeyboardInterrupt, EOFError):
                pass
        time.sleep(0.01)


def __dir__():
    return (
        'Buffer',
        'Clients',
        'Display',
        'Output',
        'Screen'
    )
