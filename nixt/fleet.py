# This file is placed in the Public Domain.


"client"


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


def __dir__():
    return (
        'Fleet',
    )
