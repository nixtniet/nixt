# This file is placed in the Public Domain.


"clients"


import _thread


from .handler import Handler


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.lock = _thread.allocate_lock()
        Fleet.add(self)

    def announce(self, txt):
        pass

    def raw(self, txt):
        raise NotImplementedError("raw")

    def say(self, channel, txt):
        self.raw(txt)


"fleet"


class Fleet:

    clients = {}

    @staticmethod
    def add(clt):
        Fleet.clients[repr(clt)] = clt

    @staticmethod
    def all():
        return Fleet.clients.values()

    @staticmethod
    def announce(txt):
        for clt in Fleet.clients.values():
            clt.announce(txt)

    @staticmethod
    def display(evt):
        clt = Fleet.get(evt.orig)
        if not clt:
            return
        with clt.lock:
            for tme in sorted(evt.result):
                clt.say(evt.channel, evt.result[tme])

    @staticmethod
    def first():
        clt =  list(Fleet.clients.values())
        res = None
        if clt:
            res = clt[0]
        return res

    @staticmethod
    def get(orig):
        return Fleet.clients.get(orig, None)

    @staticmethod
    def say(orig, channel, txt):
        clt = Fleet.get(orig)
        if clt:
            clt.say(channel, txt)

    @staticmethod
    def wait():
        for clt in Fleet.clients.values():
            if "wait" in dir(clt):
                clt.wait()


"interface"


def __dir__():
    return (
        'Client',
        'Fleet'
    )
