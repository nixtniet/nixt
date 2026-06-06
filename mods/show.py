# This file is placed in the Public Domain.


"locate objects"


import threading
import time


from nixt.defines import Broker, Commands, Locate, Main, Md5
from nixt.defines import Mods, Object, Time, Workdir


whitelist = ['cmd', 'fields', 'fleet', 'objects', 'threads', 'uptime', 'version']


def cmd(event):
    "list available commands."
    event.reply(",".join(sorted(Mods.completions or Commands.cmds)))


def fields(event):
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


def fleet(event):
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
        event.reply(' | '.join([Object.fqn(o).split(".")[-1] for o in clts]))
        return
    if index < len(clts):
        event.reply(str(clts[index]))
    else:
        event.reply("no matching client.")


def objects(event):
    "find objects."
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in Workdir.kinds()])
        if res:
            event.reply(",".join(res))
        else:
            event.reply("no data.")
        return
    otype = event.args[0]
    nmr = 0
    for fnm, obj in sorted(
                           Locate.find(otype, event.gets),
                           key=lambda x: Time.fntime(x[0])
                          ):
        diff = time.time()-Time.fntime(fnm)
        event.reply(f"{nmr} {Object.fmt(obj)} {Time.elapsed(diff)}")
        nmr += 1
    if not nmr:
        event.reply("no result")


def threads(event):
    "list of running threads."
    result = []
    for thread in sorted(threading.enumerate(), key=lambda x: x.name):
        if str(thread).startswith("<_"):
            continue
        if getattr(thread, "state", None) and getattr(thread, "sleep", None):
            upt = thread.sleep - int(time.time() - thread.state["latest"])
        elif getattr(thread, "starttime", None):
            upt = time.time() - thread.starttime
        else:
            upt = time.time() - Time.starttime
        result.append((upt, thread.name))
    res = []
    for upt, txt in sorted(result, key=lambda x: x[0]):
        lap = Time.elapsed(upt)
        res.append(f"{txt}/{lap}")
    if res:
        event.reply(" ".join(res))
    else:
        event.reply("no threads")


def uptime(event):
    "show uptiome."
    event.reply(Time.elapsed(time.time()-Time.starttime))


def version(event):
    "show verson."
    event.reply(f"{Main.name.upper()} {Md5.core()}")
