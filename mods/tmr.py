# This file is placed in the Public Domain.


import datetime
import logging
import random
import re
import time


from nixt.brokers import Broker
from nixt.locater import Locater
from nixt.objects import Object, items
from nixt.repeats import Timed
from nixt.persist import Disk
from nixt.statics import MONTH
from nixt.utility import Time, Utils
from nixt.workdir import Workdir


rand = random.SystemRandom()


def init():
    Timers.path = Locater.last(Timers.timers) or Workdir.path(Timers.timers)
    remove = []
    for tme, args in items(Timers.timers):
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


class NoDate(Exception):

    pass


class Timer(Object):

    pass


class Timers(Object):

    path = ""
    timers = Timer()

    @staticmethod
    def add(tme, orig, channel,  txt):
        setattr(Timers.timers, str(tme), (orig, channel, txt))

    @staticmethod
    def delete(tme):
         delattr(Timers.timers, str(tme))


def tmr(event):
    result = ""
    if not event.rest:
        nmr = 0
        for tme, txt in Object.items(Timers.timers):
            lap = float(tme) - time.time()
            if lap > 0:
                event.reply(f'{nmr} {" ".join(txt)} {Utils.elapsed(lap)}')
                nmr += 1
        if not nmr:
            event.reply("no timers.")
        return result
    seconds = 0
    line = ""
    for word in event.args:
        if word.startswith("+"):
            try:
                seconds = int(word[1:])
            except (ValueError, IndexError):
                event.reply(f"{seconds} is not an integer")
                return result
        else:
            line += word + " "
    if seconds:
        target = time.time() + seconds
    else:
        try:
            target = get_day(event.rest)
        except NoDate:
            target = to_day(today())
        hour =  get_hour(event.rest)
        if hour:
            target += hour
    target += rand.random() 
    if not target or time.time() > target:
        event.reply("already passed given time.")
        return result
    diff = target - time.time()
    txt = " ".join(event.args[1:])
    Timers.add(target, event.orig, event.channel, txt)
    Disk.write(Timers.timers, Timers.path or Workdir.path(Timers.timers))
    bot = getobj(event.orig)
    timer = Timed(diff, bot.say, event.orig, event.channel, txt)
    timer.start()
    event.reply("ok " + Utils.elapsed(diff))
