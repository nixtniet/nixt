# This file is placed in the Public Domain.


"timers"


import logging
import random
import threading
import time


from nixt.brokers import Broker
from nixt.objects import Base, Object, Methods
from nixt.persist import Disk, Locate
from nixt.threads import Thread, Timed
from nixt.utility import Time


rand = random.SystemRandom()


def init():
    Timers.start()
    logging.info(f"{len(Timers.timers)} timers")


class Timer(Base):

    pass


class Timers(Base):

    path = ""
    running = threading.Event()
    timers = Timer()
    lock = threading.RLock()

    @classmethod
    def add(cls, tme, orig, channel,  txt):
        with Timers.lock:
            setattr(Timers.timers, str(tme), (orig, channel, txt))

    @classmethod
    def delete(cls, tme):
        with Timers.lock:
            delattr(Timers.timers, str(tme))

    @classmethod
    def loop(cls):
        while cls.running.is_set():
            time.sleep(1.0)
            timed = time.time()
            for tme, args in Object.items(cls.timers):
                if float(tme) < timed:
                    Thread.launch(cls.run, args) 

    @classmethod
    def run(cls, args):
        orig, channel, txt = args
        for origin, bot in Broker.like(orig):
            if not origin or not bot:
                continue
            bot.say(channel, txt)

    @classmethod
    def start(cls):
        cls.path = Locate.last(cls.timers) or Methods.ident(cls.timers)
        cls.running.set()
        Thread.launch(cls.loop)

    @classmethod
    def stop(cls):
        cls.running.clear()
        Disk.write(cls.timers, cls.path)


def tmr(event):
    if not event.rest:
        event.reply("tmr <date> <txt>")
        return
    todo = Time.extract(event.rest)
    if not todo:
        event.reply("can't determine time")
        return
    todo += rand.random()
    if not todo or time.time() > todo:
        event.reply("already passed given time.")
        return
    diff = todo - time.time()
    txt = " ".join(event.args[1:])
    Timers.add(todo, event.orig, event.channel, txt)
    with Timers.lock:
        Disk.write(Timers.timers, Timers.path or Methods.ident(Timers.timers))
    bot = Broker.get(event.orig)
    if not bot:
        event.reply("no bot")
        return
    timer = Timed(diff, bot.say, event.channel, txt)
    timer.start()
    event.reply("ok " + Time.elapsed(diff))
