# This file is placed in the Public Domain.


"configuration"


from nixt.objects import Data, Methods, Object
from nixt.package import Mods
from nixt.persist import Cfg


def cfg(event):
    if not event.args:
        mods = f"cfg <{Mods.has('Config') + ',main'}>"
        if mods.startswith(","):
            mods = mods[1:]
        event.reply(mods)
        return
    name = event.args[0]
    config = Data()
    Cfg.load(config, name)
    if name != "main" and not config:
        mod = Mods.get(name)
        if not mod:
            event.reply(f"no {name} module found.")
            return
        config = getattr(mod, "Config", None)
        if not config:
            event.reply("no configuration found.")
            return
    if not event.sets:
        event.reply(
            Methods.fmt(
                config,
                Object.keys(config),
                skip=["word",]
            )
        )
        return
    Methods.edit(config, event.sets)
    Cfg.save(config, name)
    mod = Mods.get(name)
    if mod and "configure" in dir(mod):
        mod.configure()
    event.ok()


cfg.skip = "irc"


def krn(event):
    txt = "cfg main " + event.rest
    Methods.parse(event, txt)
    cfg(event)


krn.skip = "irc"
