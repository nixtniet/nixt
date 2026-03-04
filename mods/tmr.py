# This file is placed in the Public Domain.
# pylint: disable=R0903


"timers"


import logging
import random
import threading
import time


from nixt.methods import ident
from nixt.objects import Object, items
from nixt.runtime import broker, db
from nixt.threads import Timed
from nixt.utility import NoDate, day, elapsed, extract, hour, today


rand = random.SystemRandom()


def configure():
    Timers.path = db.first(Timers.timers) or ident(Timers.timers)


def init():
    "initialisze timers."
    remove = []
    for tme, args in items(Timers.timers):
        if not args:
            continue
        orig, channel, txt = args
        for origin in broker.like(orig):
            if not origin:
                continue
            diff = float(tme) - time.time()
            if diff > 0:
                bot = broker.get(origin)
                timer = Timed(diff, bot.say, channel, txt)
                timer.start()
            else:
                remove.append(tme)
    for tme in remove:
        Timers.delete(tme)
    if Timers.timers:
        db.write(Timers.timers, Timers.path)
    logging.warning("%s timers", len(Timers.timers))


class Timer(Object):

    """Timer"""


class Timers(Object):

    """Timers"""

    path = ""
    timers = Timer()
    lock = threading.RLock()

    @staticmethod
    def add(tme, orig, channel, txt):
        "add a timer."
        with Timers.lock:
            setattr(Timers.timers, str(tme), (orig, channel, txt))

    @staticmethod
    def delete(tme):
        "delete a timer."
        with Timers.lock:
            delattr(Timers.timers, str(tme))


def tmr(event):
    "timer command."
    if not event.rest:
        nmr = 0
        for tme, txt in items(Timers.timers):
            lap = float(tme) - time.time()
            if lap > 0:
                event.reply(f'{nmr} {" ".join(txt)} {elapsed(lap)}')
                nmr += 1
        return
    seconds = 0
    line = ""
    for word in event.args:
        if word.startswith("+"):
            try:
                seconds = int(word[1:])
            except (ValueError, IndexError):
                event.reply(f"{seconds} is not an integer")
                return
        else:
            line += word + " "
    if seconds:
        target = time.time() + seconds
    else:
        try:
            target = day(event.rest)
        except NoDate:
            target = extract(today())
        hours =  hour(event.rest)
        if hours:
            target += hours
    target += rand.random()
    if not target or time.time() > target:
        event.reply("already passed given time.")
        return
    diff = target - time.time()
    txt = " ".join(event.args[1:])
    Timers.add(target, event.orig, event.channel, txt)
    db.write(Timers.timers, Timers.path or ident(Timers.timers))
    bot = broker.get(event.orig)
    timer = Timed(diff, bot.say, event.channel, txt)
    timer.start()
    event.reply("ok " + elapsed(diff))
