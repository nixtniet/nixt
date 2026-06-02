# This file is placed in the Public Domain.


"administrator"


import inspect
import os
import threading
import time


from nixt.defines import Base, Broker, Disk, Json, Main, Md5, Mods
from nixt.defines import Object, Time, d, j


def config(event):
    "configure modules."
    if not event.args:
        mods = f"{'main,' + Mods.has('Config')}"
        if mods.endswith(","):
            mods = mods[:-1]
        event.iface(f"config <{mods}>")
        return
    name = event.args[0]
    cfg = Base()
    Disk.read(cfg, name, "config")
    if name != "main" and not cfg:
        mod = Mods.get(name)
        if not mod:
            event.reply(f"no {name} module found.")
            return
        cfg = getattr(mod, "Config", None)
        if not cfg:
            event.reply("no configuration found.")
            return
    if not event.sets:
        event.reply(
            Object.fmt(
                cfg,
                Object.keys(cfg),
                skip=["word",]
            )
        )
        return
    Object.edit(config, event.sets)
    Disk.write(config, name, "config")
    event.ok()


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


def service(event):
    "generate systemd service file."
    import getpass
    name = getpass.getuser()
    event.reply(SYSTEMD % (
                           Main.name.upper(),
                           name,
                           name,
                           name,
                           Main.name
                          ))


def table(event):
    "create table."
    core = {}
    md5s = {}
    for name in Mods.list():
        module = Mods.get(name)
        md5s[name] = Md5.md5(module.__file__)
    corepath = d(inspect.getsourcefile(Mods))
    for path in os.listdir(corepath):
        if path.startswith("__") or not path.endswith(".py") or "statics" in path:
            continue
        name = path[:-3]
        core[name] = Md5.md5(j(corepath, path))
    event.reply("# This file is placed in the Public Domain.")
    event.reply("\n")
    event.reply('"static tables"')
    event.reply("\n")
    event.reply(f"CORE = {Json.dumps(core, indent=4, sort_keys=True)}")
    event.reply("\n")
    event.reply(f"MODULES = {Json.dumps(md5s, indent=4, sort_keys=True)}")


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


SYSTEMD = """[Unit]
Description=%s
After=multi-user.target

[Service]
Type=simple
User=%s
Group=%s
ExecStart=/home/%s/.local/bin/%s -s

[Install]
WantedBy=multi-user.target"""
