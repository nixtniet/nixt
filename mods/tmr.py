# This file is placed in the Public Domain.


"timers"


import logging
import random
import threading
import time


from nixt.defines import Base, Broker, Disk, Locate, Object, Thread, Time


rand = random.SystemRandom()


def init():
    "intialize the timer module."
    TimerLoop.start()
    logging.warning("%s timers" , len(TimerLoop.timers))


def shutdown():
    "shutdown timer module."
    TimerLoop.stop()


class Timers(Base):

    pass


class TimerLoop:

    dosave = False
    lock = threading.RLock()
    path = ""
    running = threading.Event()
    timers = Timers()

    @classmethod
    def add(cls, tme, orig, channel,  txt):
        "add a timer."
        with cls.lock:
            setattr(cls.timers, str(tme), (orig, channel, txt))

    @classmethod
    def delete(cls, tme):
        "delete a timer."
        with cls.lock:
            delattr(cls.timers, str(tme))

    @classmethod
    def loop(cls):
        "timer loop."
        while cls.running.is_set():
            time.sleep(1.0)
            timed = time.time()
            remove = []
            for tme, args in Object.items(cls.timers):
                if float(tme) < timed:
                    Thread.launch(cls.run, args)
                    remove.append(tme)
            for tme in remove:
                cls.dosave = True
                cls.delete(tme)

    @classmethod
    def run(cls, args):
        "run a timer."
        orig, channel, txt = args
        for origin, bot in Broker.like(orig):
            if not origin or not bot:
                continue
            bot.say(channel, txt)

    @classmethod
    def start(cls):
        "start timers."
        cls.path = Locate.first(cls.timers) or Disk.ident(cls.timers)
        cls.running.set()
        Thread.launch(cls.loop, name="Timers.loop")

    @classmethod
    def stop(cls):
        "stop timers."
        cls.running.clear()
        if cls.timers or cls.dosave:
            Disk.write(cls.timers, cls.path)


class Cmd:

    def add(event):
        "add a timer."
        if not event.rest:
            event.reply("timer add <date> <txt>")
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
        TimerLoop.add(todo, Object.fqn(bot), event.channel, txt)
        event.ok(Time.elapsed(diff))
