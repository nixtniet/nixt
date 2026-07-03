# This file is placed in the Public Domain.


"locate objects"


import threading
import time


from nixt.defines import Broker, Locate, Main, Md5, Mods
from nixt.defines import Method, Time, Workdir


def cmd(event):
    "list available commands."
    event.reply(",".join(sorted(Mods.cmds)))


def fie(event):
    "show fields of a type."
    if not event.rest:
        res = sorted({x.split('.')[-1].lower() for x in Workdir.kinds()})
        if res:
            event.reply(",".join(res))
        else:
            event.reply("no types")
        return
    itms = Locate.attrs(event.args[0])
    if not itms:
        event.reply("no attributes")
    else:
        event.reply(",".join(itms))


def flt(event):
    "list of running clients."
    try:
        index = int(event.args[0])
    except (IndexError, ValueError):
        index = None
    clts = list(Broker.objs("announce"))
    if not clts:
        event.reply("no clients")
        return
    if index is None:
        event.reply(' | '.join([Method.fqn(o).split(".")[-1] for o in clts]))
        return
    if index < len(clts):
        event.reply(str(clts[index]))
    else:
        event.reply("no matching client.")


def thr(event):
    "list of running threads."
    result = []
    for thread in sorted(threading.enumerate(), key=lambda x: x.name):
        if str(thread).startswith("<_"):
            continue
        if getattr(thread, "state", None) and getattr(thread, "sleep", None):
            uptime = thread.sleep - int(time.time() - thread.state["latest"])
        elif getattr(thread, "starttime", None):
            uptime = time.time() - thread.starttime
        else:
            uptime = time.time() - Time.starttime
        result.append((uptime, thread.name))
    res = []
    for uptime, txt in sorted(result, key=lambda x: x[0]):
        lap = Time.elapsed(uptime)
        res.append(f"{txt}/{lap}")
    if res:
        event.reply(" ".join(res))
    else:
        event.reply("no threads")


def upt(event):
    "show uptiome."
    event.reply(Time.elapsed(time.time()-Time.starttime))


def ver(event):
    "show verson."
    event.reply(f"{Main.name.upper()} {Md5.core()}")
