# This file is placed in the Public Domain.


"timers"


import logging
import random
import threading
import time


from nixt.brokers import Broker
from nixt.objects import Data, Object, Methods
from nixt.persist import Disk, Locate
from nixt.threads import Thread, Timed
from nixt.utility import Time


rand = random.SystemRandom()


def init():
    Timers.path = Locate.last(Timers.timers) or Methods.ident(Timers.timers)
    remove = []
    for tme, args in Object.items(Timers.timers):
        if not args:
            continue
        orig, channel, txt = args
        for origin in Broker.like(orig):
            if not origin:
                continue
            diff = float(tme) - time.time()
            if diff > 0:
                bot = Broker.get(origin)
                timer = Timed(diff, bot.say, channel, txt)
                timer.start()
            else:
                remove.append(tme)
    for tme in remove:
        Timers.delete(tme)
    if Timers.timers:
        Disk.write(Timers.timers, Timers.path)
    logging.warning("%s timers", len(Timers.timers))


class Timer(Data):

    pass


class Timers(Data):

    path = ""
    timers = Timer()
    lock = threading.RLock()

    @staticmethod
    def add(tme, orig, channel,  txt):
        with Timers.lock:
            setattr(Timers.timers, str(tme), (orig, channel, txt))

    @staticmethod
    def delete(tme):
        with Timers.lock:
            delattr(Timers.timers, str(tme))


def tmr(event):
    if not event.rest:
        nmr = 0
        for tme, txt in Object.items(Timers.timers):
            lap = float(tme) - time.time()
            if lap > 0:
                event.reply(f'{nmr} {" ".join(txt)} {Time.elapsed(lap)}')
                nmr += 1
        if not nmr:
            event.reply("no timers.")
        return
    target = Time.extract(event.rest)
    if not target:
        event.reply("can't determine time")
        return
    target += rand.random()
    if not target or time.time() > target:
        event.reply("already passed given time.")
        return
    diff = target - time.time()
    txt = " ".join(event.args[1:])
    Timers.add(target, event.orig, event.channel, txt)
    Disk.write(Timers.timers, Timers.path or Methods.ident(Timers.timers))
    bot = Broker.get(event.orig)
    timer = Timed(diff, bot.say, event.channel, txt)
    Thread.launch(timer.start).join()
    event.reply("ok " + Time.elapsed(diff))
