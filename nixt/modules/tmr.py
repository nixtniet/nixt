# This file is placed in the Public Domain.


"timers"


import time as ttime


from ..object  import update
from ..persist import elapsed, find, ident, store, write
from ..handler import Event, Fleet
from ..thread  import Timer, launch
from ..time    import NoDate, get_day, get_hour, to_day, today


def init():
    for _fn, obj in find("timer"):
        if "time" not in dir(obj):
            continue
        diff = float(obj.time) - ttime.time()
        if diff > 0:
            evt = Event()
            update(evt, obj)
            timer = Timer(diff, Fleet.announce, evt.rest)
            timer.start()


def tmr(event):
    result = ""
    if not event.rest:
        nmr = 0
        for _fn, obj in find('timer'):
            lap = float(obj.time) - ttime.time()
            if lap > 0:
                event.reply(f'{nmr} {obj.txt} {elapsed(lap)}')
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
        target = ttime.time() + seconds
    else:
        try:
            target = get_day(event.rest)
        except NoDate:
            target = to_day(today())
        hour =  get_hour(event.rest)
        if hour:
            target += hour
    if not target or ttime.time() > target:
        event.reply("already passed given time.")
        return result
    event.time = target
    diff = target - ttime.time()
    event.reply("ok " +  elapsed(diff))
    del event.args
    event.reply(event.rest)
    timer = Timer(diff, event.display)
    update(timer, event)
    write(timer, store(ident(timer)))
    launch(timer.start)
    return result
