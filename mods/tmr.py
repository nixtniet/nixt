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
    TimerLoop.start()
    logging.warning(f"{len(TimerLoop.timers)} timers")


def shutdown():
    TimerLoop.stop()


class Timers(Base):

    pass


class TimerLoop:

    path = ""
    running = threading.Event()
    timers = Timers()
    lock = threading.RLock()

    @classmethod
    def add(cls, tme, orig, channel,  txt):
        with cls.lock:
            setattr(cls.timers, str(tme), (orig, channel, txt))

    @classmethod
    def delete(cls, tme):
        with cls.lock:
            delattr(cls.timers, str(tme))

    @classmethod
    def loop(cls):
        while cls.running.is_set():
            time.sleep(1.0)
            timed = time.time()
            remove = []
            for tme, args in Object.items(cls.timers):
                if float(tme) < timed:
                    Thread.launch(cls.run, args)
                    remove.append(tme)
            for tme in remove:
                cls.delete(tme)

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
        Thread.launch(cls.loop, name="Timers.loop")

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
    bot = Broker.get(event.orig)
    TimerLoop.add(todo, Methods.fqn(bot), event.channel, txt)
    event.ok(Time.elapsed(diff))